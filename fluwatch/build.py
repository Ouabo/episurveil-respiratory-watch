"""Raw open data -> small processed tables used by the app (data/processed/*.parquet).

Run: python -m fluwatch.build            (uses data/raw as is)
     python -m fluwatch.build --download (fetches fresh copies first)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

import pandas as pd

from .sources import GEO, PROCESSED, RAW, download_all
from .status import season_of, season_week, wastewater_status, week_to_date, weekly_status

STATE_CODES = {"Baden-Württemberg": "BW", "Baden-Wuerttemberg": "BW", "Bayern": "BY", "Berlin": "BE",
               "Brandenburg": "BB", "Bremen": "HB", "Hamburg": "HH", "Hessen": "HE",
               "Mecklenburg-Vorpommern": "MV", "Niedersachsen": "NI", "Nordrhein-Westfalen": "NW",
               "Rheinland-Pfalz": "RP", "Saarland": "SL", "Sachsen": "SN", "Sachsen-Anhalt": "ST",
               "Schleswig-Holstein": "SH", "Thüringen": "TH", "Thueringen": "TH",
               "Deutschland": "DE", "Bundesweit": "DE"}
STATE_NAMES = {"BW": "Baden-Württemberg", "BY": "Bayern", "BE": "Berlin", "BB": "Brandenburg", "HB": "Bremen",
               "HH": "Hamburg", "HE": "Hessen", "MV": "Mecklenburg-Vorpommern", "NI": "Niedersachsen",
               "NW": "Nordrhein-Westfalen", "RP": "Rheinland-Pfalz", "SL": "Saarland", "SN": "Sachsen",
               "ST": "Sachsen-Anhalt", "SH": "Schleswig-Holstein", "TH": "Thüringen", "DE": "Deutschland"}


def _add_calendar(d: pd.DataFrame) -> pd.DataFrame:
    return d.assign(season=season_of(d["date"]).values, sweek=season_week(d["date"]).values)


def build_europe() -> pd.DataFrame:
    d = pd.read_csv(RAW / "ecdc_iliari.csv")
    d = d[d["age"] == "total"].copy()
    d["date"] = week_to_date(d["yearweek"])
    d = _add_calendar(d)
    cur = d["season"].max()
    # one measure per country: flu-like illness (ILI) if reported this season, else respiratory infections (ARI)
    has_ili = set(d[(d["indicator"] == "ILIconsultationrate") & (d["season"] == cur)]["countryname"])
    d["keep"] = [(ind == "ILIconsultationrate") == (c in has_ili) for c, ind in zip(d["countryname"], d["indicator"])]
    d = d[d["keep"]].rename(columns={"countryname": "country"})
    d["measure"] = d["indicator"].map({"ILIconsultationrate": "ILI", "ARIconsultationrate": "ARI"})
    return d[["country", "measure", "yearweek", "date", "season", "sweek", "value"]].sort_values(["country", "date"])


def build_de_are() -> pd.DataFrame:
    d = pd.read_csv(RAW / "are.tsv", sep="\t", encoding="utf-8")
    d = d[d["Altersgruppe"] == "00+"].copy()
    d["state"] = d["Bundesland"].map(STATE_CODES)
    d["date"] = week_to_date(d["Kalenderwoche"])
    d = _add_calendar(d).rename(columns={"ARE_Konsultationsinzidenz": "value", "Kalenderwoche": "yearweek"})
    return d[["state", "yearweek", "date", "season", "sweek", "value"]].sort_values(["state", "date"])


def build_de_flu() -> pd.DataFrame:
    d = pd.read_csv(RAW / "flu.tsv", sep="\t", encoding="utf-8")
    d = d[d["Altersgruppe"] == "00+"].copy()
    d["state"] = d["Region"].map(STATE_CODES)
    # the RKI file leaves out weeks with zero cases: put them back as 0
    full = pd.MultiIndex.from_product([sorted(d["state"].unique()), sorted(d["Meldewoche"].unique())],
                                      names=["state", "Meldewoche"])
    d = d.set_index(["state", "Meldewoche"])[["Fallzahl", "Inzidenz"]].reindex(full, fill_value=0).reset_index()
    d["date"] = week_to_date(d["Meldewoche"])
    d = _add_calendar(d).rename(columns={"Inzidenz": "value", "Fallzahl": "cases", "Meldewoche": "yearweek"})
    return d[["state", "yearweek", "date", "season", "sweek", "value", "cases"]].sort_values(["state", "date"])


def build_de_grippeweb() -> pd.DataFrame:
    d = pd.read_csv(RAW / "grippeweb.tsv", sep="\t", encoding="utf-8")
    d = d[(d["Altersgruppe"] == "00+") & (d["Region"] == "Bundesweit")].copy()
    d["date"] = week_to_date(d["Kalenderwoche"])
    d = _add_calendar(d).rename(columns={"Inzidenz": "value", "Erkrankung": "illness", "Kalenderwoche": "yearweek"})
    return d[["illness", "yearweek", "date", "season", "sweek", "value"]].sort_values(["illness", "date"])


def build_wastewater() -> pd.DataFrame:
    cols = ["standort", "bundesland", "datum", "viruslast", "vorhersage", "einwohner", "typ", "unter_bg"]
    d = pd.read_csv(RAW / "amelag_sites.tsv", sep="\t", usecols=cols, encoding="utf-8", low_memory=False)
    d["datum"] = pd.to_datetime(d["datum"])
    d = d[d["datum"] >= "2023-01-01"]
    d["below"] = d["unter_bg"].map({"ja": True, "nein": False})
    # RKI flags a combined A+B value as below the detection limit if EITHER part is below;
    # "barely detectable" here means BOTH parts are below.
    key = ["standort", "datum"]

    def both_below(a, b, combined):
        pa = d[d["typ"] == a].set_index(key)["below"].astype("boolean")
        pb = d[d["typ"] == b].set_index(key)["below"].astype("boolean")
        c = d[d["typ"] == combined].copy()
        idx = c.set_index(key).index
        c["below"] = (pa.reindex(idx).fillna(True) & pb.reindex(idx).fillna(True)).values & c["viruslast"].notna().values
        return c

    flu = both_below("Influenza A", "Influenza B", "Influenza A+B").assign(pathogen="flu")
    cov = d[d["typ"] == "SARS-CoV-2"].assign(pathogen="covid")
    rsv_ab = both_below("RSV A", "RSV B", "RSV A+B")
    rsv_old = d[(d["typ"] == "RSV A/B") & ~d.set_index(["standort", "datum"]).index.isin(
        rsv_ab.set_index(["standort", "datum"]).index)]
    rsv = pd.concat([rsv_ab, rsv_old]).assign(pathogen="rsv")
    w = pd.concat([flu, rsv, cov]).rename(columns={
        "standort": "site", "bundesland": "state", "datum": "date", "viruslast": "measured",
        "vorhersage": "smooth", "einwohner": "population"})
    w["below"] = w["below"].astype("boolean")
    return w[["site", "state", "pathogen", "date", "measured", "smooth", "below", "population"]].sort_values(
        ["site", "pathogen", "date"]).reset_index(drop=True)


def main(download: bool = False):
    if download:
        download_all(max_age_hours=0)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    eu, are, flu, gw, ww = build_europe(), build_de_are(), build_de_flu(), build_de_grippeweb(), build_wastewater()
    eu_s = weekly_status(eu, "country", exclude_seasons=())
    eu_s = eu_s.merge(eu.groupby("country")["measure"].first().reset_index(), on="country")
    are_s = weekly_status(are, "state")
    flu_s = weekly_status(flu, "state", exclude_seasons=("2019/20", "2020/21", "2021/22"))
    gw_s = weekly_status(gw, "illness")
    ww_s = wastewater_status(ww)
    sites = pd.read_csv(GEO / "ww_sites.csv") if (GEO / "ww_sites.csv").exists() else None
    if sites is not None:
        ww_s = ww_s.merge(sites[["standort", "lat", "lon"]].rename(columns={"standort": "site"}), on="site", how="left")
    for name, df in {"eu": eu, "eu_status": eu_s, "de_are": are, "de_are_status": are_s, "de_flu": flu,
                     "de_flu_status": flu_s, "de_grippeweb": gw, "de_grippeweb_status": gw_s,
                     "ww": ww, "ww_status": ww_s}.items():
        df.to_parquet(PROCESSED / f"{name}.parquet", index=False)
    meta = {
        "built_utc": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "eu_latest_week": str(eu["yearweek"].max()), "de_are_latest_week": str(are["yearweek"].max()),
        "de_flu_latest_week": str(flu["yearweek"].max()), "de_grippeweb_latest_week": str(gw["yearweek"].max()),
        "ww_latest_date": str(ww.loc[ww["measured"].notna(), "date"].max().date()),
    }
    (PROCESSED / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main(download="--download" in sys.argv)
