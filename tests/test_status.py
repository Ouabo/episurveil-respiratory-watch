import numpy as np
import pandas as pd

from fluwatch.status import level_of, season_of, season_week, trend_of, weekly_status, week_to_date


def test_calendar():
    d = week_to_date(pd.Series(["2026-W40", "2026-W45", "2027-W02", "2026-W39"]))
    assert list(season_of(d)) == ["2026/27", "2026/27", "2026/27", "2025/26"]
    assert list(season_week(d))[:3] == [0, 5, 15]   # 2026 has 53 ISO weeks


def test_level_bands():
    thr = (10.0, 20.0, 30.0)
    assert [level_of(v, thr) for v in (5, 10, 25, 30, 99)] == ["low", "moderate", "high", "very_high", "very_high"]
    assert level_of(5, None) is None


def test_trend():
    assert trend_of(115, 100, 0.15) == "rising"
    assert trend_of(110, 100, 0.15) == "stable"
    assert trend_of(86, 100, 0.15) == "falling"
    assert trend_of(0.3, 0.1, 0.15, min_abs=0.5) == "stable"   # tiny numbers do not make a trend
    assert trend_of(np.nan, 100, 0.15) is None


def _series(place, weeks, values):
    return pd.DataFrame({"place": place, "date": week_to_date(pd.Series(weeks)), "value": values})


def test_weekly_status_uses_past_seasons_only_and_flags_stale():
    weeks, vals = [], []
    for y in (2022, 2023, 2024, 2025):           # four past seasons, flat at 100 with a peak of 300
        for w in range(40, 53):
            weeks.append(f"{y}-W{w:02d}"); vals.append(100.0)
        for w in range(1, 21):
            weeks.append(f"{y + 1}-W{w:02d}"); vals.append(300.0 if w == 5 else 100.0)
    weeks += ["2026-W40", "2026-W41", "2026-W42", "2026-W43"]
    vals += [100.0, 100.0, 400.0, 400.0]
    a = _series("A", weeks, vals)
    b = _series("B", weeks[:-12], vals[:-12])     # stops reporting three months earlier
    s = weekly_status(pd.concat([a, b]), "place").set_index("place")
    assert s.loc["A", "level"] == "very_high" and s.loc["A", "trend"] == "rising" and s.loc["A", "fresh"]
    assert not s.loc["B", "fresh"] and s.loc["B", "level"] is None


def test_wastewater_barely_detectable_and_stale():
    from fluwatch.status import wastewater_status
    dates = pd.date_range("2026-09-01", "2026-11-04", freq="3D")
    rows = []
    for site, below, last in [("A", True, dates[-1]), ("B", False, dates[-1]), ("C", False, pd.Timestamp("2026-09-10"))]:
        for i, d in enumerate(dates):
            if d > last:
                continue
            v = 100.0 if below else 100.0 * (1.1 ** i)
            rows.append({"site": site, "state": "BE", "pathogen": "flu", "date": d, "measured": v,
                         "smooth": v, "below": below, "population": 1000})
    s = wastewater_status(pd.DataFrame(rows)).set_index("site")
    assert s.loc["A", "not_detected"] and s.loc["A", "trend"] == "stable"
    assert s.loc["B", "trend"] == "rising" and not s.loc["B", "not_detected"]
    assert not s.loc["C", "fresh"] and s.loc["C", "trend"] is None
