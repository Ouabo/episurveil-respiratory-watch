"""One-off: find map coordinates for the AMELAG wastewater sites (OpenStreetMap Nominatim).

Usage: python scripts/geocode_sites.py <amelag_einzelstandorte.tsv>
Writes data/geo/ww_sites.csv (standort, bundesland, lat, lon, query, ok).
Respects the Nominatim policy: 1 request per second, generic app User-Agent, results cached.
"""
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "geo" / "ww_sites.csv"
UA = {"User-Agent": "EpiSurveil-FluWatch/0.1 (research prototype)"}
STATES = {"BW": "Baden-Württemberg", "BY": "Bayern", "BE": "Berlin", "BB": "Brandenburg", "HB": "Bremen",
          "HH": "Hamburg", "HE": "Hessen", "MV": "Mecklenburg-Vorpommern", "NI": "Niedersachsen",
          "NW": "Nordrhein-Westfalen", "RP": "Rheinland-Pfalz", "SL": "Saarland", "SN": "Sachsen",
          "ST": "Sachsen-Anhalt", "SH": "Schleswig-Holstein", "TH": "Thüringen"}


def candidates(name: str):
    n = re.sub(r"\s+\d+$", "", name).strip()          # "Hamburg 02" -> "Hamburg"
    yield n
    for sep in ["-", " ", "/"]:
        if sep in n:
            yield n.split(sep)[0]
            yield n.split(sep)[-1]


def lookup(q, state):
    r = requests.get("https://nominatim.openstreetmap.org/search",
                     params={"q": f"{q}, {state}, Deutschland", "format": "json", "limit": 1,
                             "countrycodes": "de"}, headers=UA, timeout=30)
    time.sleep(1.1)
    j = r.json() if r.ok else []
    return (float(j[0]["lat"]), float(j[0]["lon"])) if j else None


def main(tsv):
    d = pd.read_csv(tsv, sep="\t", usecols=["standort", "bundesland"], encoding="utf-8").drop_duplicates()
    done = pd.read_csv(OUT) if OUT.exists() else pd.DataFrame(columns=["standort"])
    rows = done.to_dict("records")
    for s, bl in d.itertuples(index=False):
        if s in set(done["standort"]):
            continue
        hit, used = None, None
        for q in dict.fromkeys(candidates(s)):
            hit = lookup(q, STATES[bl])
            if hit:
                used = q
                break
        rows.append({"standort": s, "bundesland": bl, "lat": hit[0] if hit else None,
                     "lon": hit[1] if hit else None, "query": used, "ok": bool(hit)})
        pd.DataFrame(rows).to_csv(OUT, index=False, encoding="utf-8")
        print(s, "->", used, hit, flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
