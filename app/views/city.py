import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from fluwatch.build import STATE_NAMES
from fluwatch.i18n import t
from fluwatch.ui import (polish, INK, LEVEL_COLORS, LINE_LAST, badge, data_date, lang, legend_html, level_label, load,
                         TREND_COLORS, show_table, states_geojson, trend_label)

L = lang()
st.title(t("city_title", L))
st.caption(t("city_intro", L))

virus = st.radio(t("pick_virus", L), ["flu", "rsv", "covid"], format_func=lambda k: t(f"v_{k}", L), horizontal=True)
ww = load("ww")
s = load("ww_status")
s = s[s["pathogen"] == virus].copy()
s["state_name"] = s["state"].map(STATE_NAMES)
s["Level"] = s.apply(lambda r: t("barely", L) if r["not_detected"] else level_label(r["level"], r["fresh"]), axis=1)
s["Trend"] = s.apply(lambda r: trend_label(r["trend"]) if r["fresh"] else "", axis=1)
s["level_key"] = s.apply(lambda r: r["level"] if r["fresh"] and isinstance(r["level"], str) else "none", axis=1)
s["trend_key"] = s.apply(lambda r: r["trend"] if r["fresh"] and isinstance(r["trend"], str) else "none", axis=1)
s["Last sample"] = s["date"].map(data_date)
s["People"] = s["population"].map(lambda v: f"{int(v):,}".replace(",", "." if L == "de" else ","))

color_by = st.radio(t("color_by", L), ["trend", "level"], format_func=lambda k: t(k, L), horizontal=True)
left, right = st.columns([1.3, 1], gap="medium")

with left:
    if color_by == "level":
        st.markdown(legend_html(), unsafe_allow_html=True)
        cmap = {k: v for k, v in LEVEL_COLORS.items() if k} | {"none": LEVEL_COLORS[None]}
        key = "level_key"
    else:
        items = "".join(
            f"<span style='display:inline-flex;align-items:center;gap:6px;margin-right:14px'>"
            f"<span style='width:14px;height:14px;border-radius:50%;background:{TREND_COLORS[k]}'></span>"
            f"{trend_label(k) if k != 'none' else t('no_recent', L)}</span>" for k in ["rising", "stable", "falling", "none"])
        st.markdown(f"<div style='font-size:0.9rem;color:{INK};margin:4px 0 8px'>{items}</div>", unsafe_allow_html=True)
        cmap, key = TREND_COLORS, "trend_key"
    m = s.dropna(subset=["lat", "lon"]).sort_values("fresh")  # grey dots drawn first, coloured on top
    fig = px.scatter_geo(m, lat="lat", lon="lon", color=key, color_discrete_map=cmap,
                         labels={"Level": t("level", L), "Trend": t("trend", L), "state_name": t("col_state", L),
                                 "Last sample": t("col_last", L)},
                         hover_name="site",
                         hover_data={key: False, "lat": False, "lon": False, "state_name": True, "Level": True,
                                     "Trend": True, "Last sample": True},
                         size=m["population"].clip(lower=50_000) ** 0.5, size_max=22)
    fig.update_traces(marker_line_color="white", marker_line_width=1)
    # state outlines underneath, drawn from the same open boundary file
    geo = states_geojson()
    base = go.Choropleth(geojson=geo, locations=[f["properties"]["shapeISO"] for f in geo["features"]],
                         featureidkey="properties.shapeISO", z=[0] * len(geo["features"]),
                         colorscale=[[0, "#F3F4F6"], [1, "#F3F4F6"]], showscale=False, hoverinfo="skip",
                         marker_line_color="#FFFFFF", marker_line_width=1.2)
    fig.add_trace(base)
    fig.data = (fig.data[-1],) + fig.data[:-1]
    fig.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
    fig.update_layout(height=620, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    st.plotly_chart(polish(fig), width="stretch", config={"displayModeBar": False}, theme=None)
    st.caption(t("only_recent", L))
    if s["lat"].isna().any():
        st.caption(t("no_coords", L))

with right:
    order = s.sort_values(["fresh", "population"], ascending=[False, False])
    labels = {r.site: f"{r.site} ({r.state_name})" for r in order.itertuples()}
    site = st.selectbox(t("search_city", L), list(labels), format_func=labels.get)
    row = s[s["site"] == site].iloc[0].to_dict()
    st.markdown(badge(row["level"], row["trend"], row["fresh"], label=t("barely", L) if row["not_detected"] else None),
                unsafe_allow_html=True)
    if row["not_detected"]:
        st.markdown(t("sentence_ww_nd", L).format(place=site, virus=t(f"v_{virus}_lc", L)))
    elif row["fresh"] and isinstance(row["level"], str):
        lv = t(row["level"], L).lower()
        tr = t(row["trend"], L).lower() if isinstance(row["trend"], str) else t("unknown_trend", L).lower()
        st.markdown(t("sentence_ww", L).format(place=site, virus=t(f"v_{virus}_lc", L), level=lv, trend=tr))
    st.caption(f"{t('as_of_day', L).format(date=row['Last sample'])} · {row['People']} {t('people_served', L)}")

    g = ww[(ww["site"] == site) & (ww["pathogen"] == virus)]
    g = g[g["date"] >= g["date"].max() - pd.Timedelta(days=365)]
    meas = g.dropna(subset=["measured"])
    fig2 = go.Figure()
    det = meas[meas["below"].fillna(False) == False]  # noqa: E712
    nd = meas[meas["below"].fillna(False) == True]  # noqa: E712
    fig2.add_trace(go.Scatter(x=det["date"], y=det["measured"], mode="markers", name=t("measured", L),
                              marker=dict(size=12, color=LINE_LAST, line=dict(color="white", width=1.5)),
                              hovertemplate="%{x|%d.%m.%Y}<extra></extra>"))
    fig2.add_trace(go.Scatter(x=nd["date"], y=nd["measured"], mode="markers", name=t("barely", L),
                              marker=dict(size=11, color="white", line=dict(color=LINE_LAST, width=2.5)),
                              hovertemplate="%{x|%d.%m.%Y}<extra></extra>"))
    sm = g[g["date"] <= meas["date"].max()] if not meas.empty else g
    fig2.add_trace(go.Scatter(x=sm["date"], y=sm["smooth"], mode="lines", name=t("smoothed", L),
                              line=dict(color=INK, width=5), hoverinfo="skip"))
    fig2.update_layout(height=480, margin=dict(l=110, r=10, t=10, b=60), plot_bgcolor="white", paper_bgcolor="white",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
                       xaxis=dict(showgrid=False, linecolor="#D1D5DB", tickformat="%b %y", dtick="M3", tickangle=0),
                       yaxis=dict(title=t("u_ww", L), gridcolor="#F0F0F0", rangemode="tozero", tickformat="~s", nticks=6))
    st.markdown(f"**{t('last_12m', L)}**")
    st.plotly_chart(polish(fig2), width="stretch", config={"displayModeBar": False}, theme=None)

with st.expander(t("show_table", L)):
    show_table(order, {"site": t("col_site", L), "state_name": t("col_state", L), "Level": t("level", L),
                       "Trend": t("trend", L), "Last sample": t("col_last", L), "People": t("col_people", L)})
