"""Shared display helpers for the Streamlit pages."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .i18n import t
from .sources import GEO, PROCESSED

# one warm hue, light -> dark (ordered magnitude); grey = no data
LEVEL_COLORS = {"low": "#FBE3C4", "moderate": "#F2A65A", "high": "#D9622B", "very_high": "#8E2A10", None: "#D6D6D6"}
LEVEL_ORDER = ["low", "moderate", "high", "very_high"]
ARROWS = {"rising": "↑", "stable": "→", "falling": "↓", None: "·"}
INK = "#1F2328"
MUTED = "#6B7280"
LINE_NOW, LINE_LAST, LINE_BEFORE = "#111111", "#5B6270", "#A3A9B3"
# trend: diverging warm (up) / cool (down) with a neutral grey middle
TREND_COLORS = {"rising": "#C2410C", "stable": "#6B7280", "falling": "#2563EB", "none": "#E5E7EB"}
TREND_BG = {"rising": "#FDE8DC", "stable": "#F1F2F4", "falling": "#E0EAFD"}
CHART_FONT = 20


def style_table(df: pd.DataFrame, level_col: str, trend_col: str, level_key: str = "level_key",
                trend_key: str = "trend_key"):
    """Pandas Styler: level cell filled with its level colour, trend cell coloured by direction.
    The key columns hold 'low'...'very_high' / 'rising'... (or 'none'); they are styled-from, not shown."""
    def row_style(r):
        out = [""] * len(r)
        cols = list(r.index)
        lk, tk = r[level_key], r[trend_key]
        if lk in LEVEL_COLORS and lk:
            fg = "#FFFFFF" if lk in ("high", "very_high") else INK
            out[cols.index(level_col)] = f"background-color:{LEVEL_COLORS[lk]};color:{fg};font-weight:600"
        else:
            out[cols.index(level_col)] = f"color:{MUTED}"
        if tk in TREND_BG:
            out[cols.index(trend_col)] = f"background-color:{TREND_BG[tk]};color:{TREND_COLORS[tk]};font-weight:700"
        return out
    return df.style.apply(row_style, axis=1)


def add_keys(s: pd.DataFrame) -> pd.DataFrame:
    """level_key / trend_key for colouring; 'none' when out of date or unknown."""
    s = s.copy()
    s["level_key"] = [lv if f and isinstance(lv, str) else "none" for lv, f in zip(s["level"], s["fresh"])]
    s["trend_key"] = [tr if f and isinstance(tr, str) else "none" for tr, f in zip(s["trend"], s["fresh"])]
    return s


def show_table(df: pd.DataFrame, columns: dict):
    """columns: source column -> header shown. Must contain 'Level' and 'Trend'; df must have the key columns."""
    d = df[list(columns) + ["level_key", "trend_key"]].rename(columns=columns)
    st.dataframe(style_table(d, columns["Level"], columns["Trend"]), hide_index=True, width="stretch",
                 column_order=list(columns.values()), height=min(36 * len(d) + 42, 640))


def lang() -> str:
    return st.session_state.get("lang", "en")


@st.cache_data(show_spinner=False)
def load(name: str) -> pd.DataFrame:
    return pd.read_parquet(PROCESSED / f"{name}.parquet")


@st.cache_data(show_spinner=False)
def meta() -> dict:
    return json.loads((PROCESSED / "meta.json").read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def states_geojson() -> dict:
    return json.loads((GEO / "de_states.geojson").read_text(encoding="utf-8"))


def _clean(v):
    return None if v is None or (isinstance(v, float) and np.isnan(v)) else v


def level_label(level, fresh=True) -> str:
    level = _clean(level)
    if fresh is False:
        return t("no_recent", lang())
    return t(level, lang()) if level else t("no_history", lang())


def trend_label(trend) -> str:
    trend = _clean(trend)
    return f"{ARROWS[trend]} {t(trend, lang())}" if trend else t("unknown_trend", lang())


def badge(level, trend, fresh=True, label=None) -> str:
    """Small HTML pill: coloured square + level text + trend arrow (identity never by colour alone)."""
    level = _clean(level) if fresh is not False else None
    col = LEVEL_COLORS[level]
    return (f"<span style='display:inline-flex;align-items:center;gap:6px;padding:2px 10px;border-radius:999px;"
            f"border:1px solid #E5E7EB;font-size:1.05rem;color:{INK}'>"
            f"<span style='width:12px;height:12px;border-radius:3px;background:{col};border:1px solid #00000022'></span>"
            f"{label or level_label(level, fresh)} &nbsp;{trend_label(trend) if fresh is not False else ''}</span>")


def sentence(place: str, measure_key: str, row) -> str:
    L = lang()
    if row is None or row.get("fresh") is False or _clean(row.get("level")) is None:
        return f"**{place}**: {level_label(None if row is None else row.get('level'), None if row is None else row.get('fresh'))}."
    measure = t(measure_key, L)
    measure_lc = measure[0].lower() + measure[1:] if L == "en" else measure
    lv = t(row["level"], L).lower()
    tr = t(row["trend"], L).lower() if _clean(row.get("trend")) else t("unknown_trend", L).lower()
    return t("sentence", L).format(place=place, measure_lc=measure_lc, level=lv, trend=tr)


def legend_html() -> str:
    L = lang()
    items = "".join(
        f"<span style='display:inline-flex;align-items:center;gap:6px;margin-right:14px'>"
        f"<span style='width:14px;height:14px;border-radius:3px;background:{LEVEL_COLORS[k]};border:1px solid #00000022'></span>"
        f"{t(k, L) if k else t('no_recent', L)}</span>" for k in LEVEL_ORDER + [None])
    return f"<div style='font-size:1rem;color:{INK};margin:4px 0 8px'>{items}</div>"


def season_chart(series: pd.DataFrame, status_row, unit: str, height: int = 500) -> go.Figure:
    """This season vs the last two, x = months Oct..Sep, background = level bands of this place."""
    L = lang()
    months = t("months", L)
    seasons = sorted(series["season"].unique())[-3:]
    names = {seasons[-1]: t("this_season", L)}
    if len(seasons) >= 2:
        names[seasons[-2]] = t("last_season", L)
    if len(seasons) >= 3:
        names[seasons[-3]] = t("season_before", L)
    styles = {t("this_season", L): (LINE_NOW, 6), t("last_season", L): (LINE_LAST, 4), t("season_before", L): (LINE_BEFORE, 3.5)}
    fig = go.Figure()
    ymax = series[series["season"].isin(seasons)]["value"].max()
    thr = None
    if status_row is not None and _clean(status_row.get("p50")) is not None:
        thr = [0, status_row["p50"], status_row["p75"], status_row["p90"], max(ymax, status_row["p90"]) * 1.08]
        for k, lo, hi in zip(LEVEL_ORDER, thr[:-1], thr[1:]):
            fig.add_hrect(y0=lo, y1=hi, fillcolor=LEVEL_COLORS[k], opacity=0.35, line_width=0, layer="below")
    for s in seasons[::-1]:
        g = series[series["season"] == s].sort_values("sweek")
        nm = names[s]
        col, w = styles[nm]
        fig.add_trace(go.Scatter(
            x=g["sweek"], y=g["value"], mode="lines", name=f"{nm} ({s})", line=dict(color=col, width=w),
            customdata=g["date"].dt.strftime("%d.%m.%Y"),
            hovertemplate=f"{nm}<br>%{{customdata}}<br>%{{y:,.1f}} {unit}<extra></extra>"))
    cur = series[series["season"] == seasons[-1]].sort_values("sweek")
    if not cur.empty:
        fig.add_trace(go.Scatter(x=[cur["sweek"].iloc[-1]], y=[cur["value"].iloc[-1]], mode="markers",
                                 marker=dict(size=16, color=LINE_NOW, line=dict(color="white", width=3)),
                                 showlegend=False, hoverinfo="skip"))
    last_x = int(cur["sweek"].max()) if not cur.empty else 0
    ticks = [0, 4, 9, 13, 17, 22, 26, 30, 35, 39, 43, 48]
    fig.update_layout(
        height=height, margin=dict(l=95, r=10, t=10, b=60), plot_bgcolor="white", paper_bgcolor="white",
        font=dict(color=INK, size=CHART_FONT), hoverlabel=dict(font_size=CHART_FONT), hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        xaxis=dict(tickvals=ticks, ticktext=months, range=[-0.5, max(33, last_x + 2)], showgrid=False,
                   linecolor="#D1D5DB"),
        yaxis=dict(title=dict(text=unit, standoff=12), automargin=True, gridcolor="#F0F0F0", rangemode="tozero",
                   range=[0, thr[-1]] if thr else None, zeroline=False))
    return fig


def polish(fig: go.Figure) -> go.Figure:
    """Larger, consistent chart text."""
    fig.update_layout(font=dict(color=INK, size=CHART_FONT, weight="bold"),
                      hoverlabel=dict(font=dict(size=CHART_FONT, weight="bold")),
                      legend=dict(font=dict(size=CHART_FONT, weight="bold")))
    fig.update_xaxes(tickfont=dict(size=CHART_FONT, weight="bold"), title_font=dict(size=CHART_FONT, weight="bold"))
    fig.update_yaxes(tickfont=dict(size=CHART_FONT, weight="bold"), title_font=dict(size=CHART_FONT, weight="bold"))
    return fig


def data_date(d) -> str:
    return pd.Timestamp(d).strftime("%d.%m.%Y")
