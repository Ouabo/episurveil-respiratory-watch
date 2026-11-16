"""Turns surveillance numbers into a plain status: level (low ... very high) and trend (rising/stable/falling).

Rule, stated once here and in plain words on the About page:
- Level: this week's value is compared with the same place's values during previous flu seasons
  (calendar weeks 40 to 20). Below the typical winter week (median) -> low; up to the 75th percentile
  -> moderate; up to the 90th -> high; above -> very high.
- Trend: the last two weeks against the two weeks before. A change of at least 15 % (weekly data)
  or 30 % (wastewater, which is noisier) counts as rising or falling.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

LEVELS = ["low", "moderate", "high", "very_high"]
TRENDS = ["falling", "stable", "rising"]


# ---------- calendar helpers ----------
def week_to_date(yearweek: pd.Series) -> pd.Series:
    """'2026-W45' -> Monday of that ISO week."""
    return pd.to_datetime(yearweek.astype(str) + "-1", format="%G-W%V-%u")


def season_of(dates: pd.Series) -> pd.Series:
    """Flu season label: weeks 40..39 of the next year, e.g. '2026/27'."""
    iso = dates.dt.isocalendar()
    start = np.where(iso.week >= 40, iso.year, iso.year - 1).astype(int)
    return pd.Series([f"{s}/{str(s + 1)[-2:]}" for s in start], index=dates.index)


def season_week(dates: pd.Series) -> pd.Series:
    """Weeks since week 40 of the season start (0 = early October)."""
    iso = dates.dt.isocalendar()
    start = np.where(iso.week >= 40, iso.year, iso.year - 1).astype(int)
    w40 = pd.to_datetime([f"{s}-W40-1" for s in start], format="%G-W%V-%u")
    return pd.Series(((dates.values - w40.values) / np.timedelta64(7, "D")).astype(int), index=dates.index)


IN_SEASON_MAX_WEEK = 32  # season week 32 = calendar week 20


# ---------- the two plain-language judgements ----------
def thresholds(history: pd.Series) -> tuple[float, float, float] | None:
    h = history.dropna()
    if len(h) < 20:
        return None
    return tuple(float(x) for x in np.percentile(h, [50, 75, 90]))


def level_of(value: float, thr) -> str | None:
    if thr is None or value is None or np.isnan(value):
        return None
    p50, p75, p90 = thr
    if value < p50:
        return "low"
    if value < p75:
        return "moderate"
    if value < p90:
        return "high"
    return "very_high"


def trend_of(recent: float, before: float, rel: float, min_abs: float = 0.0) -> str | None:
    if recent is None or before is None or np.isnan(recent) or np.isnan(before):
        return None
    change = recent - before
    if abs(change) < min_abs:
        return "stable"
    if before <= 0:
        return "rising" if recent > 0 and change >= min_abs else "stable"
    ratio = recent / before
    if ratio >= 1 + rel:
        return "rising"
    if ratio <= 1 / (1 + rel):
        return "falling"
    return "stable"


# ---------- weekly series (ECDC, RKI ARE, RKI lab flu) ----------
def weekly_status(df: pd.DataFrame, place_col: str, value_col: str = "value",
                  exclude_seasons=("2020/21", "2021/22"), rel: float = 0.15,
                  min_past_seasons: int = 2, max_past_seasons: int = 4, stale_weeks: int = 3) -> pd.DataFrame:
    """One row per place: latest week, value, level, trend, thresholds.
    df needs columns: place_col, 'date' (Monday of ISO week), value_col.
    History = the last `max_past_seasons` complete seasons (recent normal, same window for every place).
    A place whose latest week is more than `stale_weeks` behind the newest week gets fresh=False."""
    newest = df.dropna(subset=[value_col])["date"].max()
    out = []
    for place, g in df.groupby(place_col):
        g = g.dropna(subset=[value_col]).sort_values("date")
        if g.empty:
            continue
        g = g.assign(season=season_of(g["date"]).values, sweek=season_week(g["date"]).values)
        last = g.iloc[-1]
        fresh = (newest - last["date"]).days <= 7 * stale_weeks
        past = g[(g["season"] < last["season"]) & (~g["season"].isin(exclude_seasons))
                 & (g["sweek"] <= IN_SEASON_MAX_WEEK)]
        keep = sorted(past["season"].unique())[-max_past_seasons:]
        past = past[past["season"].isin(keep)]
        thr = thresholds(past[value_col]) if past["season"].nunique() >= min_past_seasons else None
        s = g.set_index("date")[value_col]
        d = last["date"]
        recent = s.reindex([d - pd.Timedelta(weeks=1), d]).mean(skipna=False)
        before = s.reindex([d - pd.Timedelta(weeks=3), d - pd.Timedelta(weeks=2)]).mean(skipna=False)
        min_abs = 0.1 * thr[0] if thr else 0.0
        out.append({
            place_col: place, "date": d, "season": last["season"], "value": float(last[value_col]),
            "fresh": bool(fresh),
            "level": level_of(float(last[value_col]), thr) if fresh else None,
            "trend": trend_of(recent, before, rel, min_abs) if fresh else None,
            "p50": thr[0] if thr else np.nan, "p75": thr[1] if thr else np.nan, "p90": thr[2] if thr else np.nan,
            "past_seasons": int(past["season"].nunique()),
        })
    return pd.DataFrame(out)


# ---------- wastewater (RKI AMELAG, per treatment plant) ----------
def wastewater_status(ww: pd.DataFrame, stale_days: int = 21, rel: float = 0.30) -> pd.DataFrame:
    """ww columns: site, state, pathogen, date, measured, smooth, below, population.
    Works on sample days only. Value = RKI's smoothed curve where it exists, else the measured sample.
    Trend: latest sample vs the last sample at least 14 days earlier.
    If the two latest samples are both below the detection limit -> 'barely detectable' (level low, stable)."""
    newest = ww.loc[ww["measured"].notna(), "date"].max()
    out = []
    for (site, pathogen), g in ww.groupby(["site", "pathogen"]):
        m = g[g["measured"].notna()].sort_values("date")
        if m.empty:
            continue
        m = m.assign(v=m["smooth"].fillna(m["measured"]))
        now = m.iloc[-1]
        earlier = m[m["date"] <= now["date"] - pd.Timedelta(days=14)]
        before = float(earlier.iloc[-1]["v"]) if not earlier.empty else np.nan
        m = m.assign(season=season_of(m["date"]).values, sweek=season_week(m["date"]).values)
        past = m[(m["season"] < m["season"].iloc[-1]) & (m["sweek"] <= IN_SEASON_MAX_WEEK)]
        thr = thresholds(past["v"]) if len(past) >= 20 else None
        fresh = (newest - now["date"]).days <= stale_days
        last2 = m["below"].tail(2)
        not_detected = bool(len(last2) == 2 and last2.fillna(False).all())
        if not fresh:
            level, trend = None, None
        elif not_detected:
            level, trend = "low", "stable"
        else:
            level, trend = level_of(float(now["v"]), thr), trend_of(float(now["v"]), before, rel)
        out.append({
            "site": site, "state": now["state"], "pathogen": pathogen, "population": now["population"],
            "date": now["date"], "value": float(now["v"]), "fresh": fresh, "not_detected": not_detected and fresh,
            "level": level, "trend": trend,
        })
    return pd.DataFrame(out)
