import plotly.express as px
import streamlit as st

from fluwatch.build import STATE_NAMES
from fluwatch.i18n import t
from fluwatch.ui import (PLOT_CONFIG, phone_height, polish, LEVEL_COLORS, add_keys, show_table, badge, data_date, lang, legend_html, level_label, load, season_chart,
                         sentence, states_geojson, trend_label)

L = lang()
st.title(t("de_title", L))
st.caption(t("de_intro", L))

measure = st.radio(t("pick_measure", L), ["are", "flu"], format_func=lambda k: t(f"m_{k}", L), horizontal=True)
st.caption(t(f"measure_note_{measure}", L))
series = load("de_are" if measure == "are" else "de_flu")
s = load("de_are_status" if measure == "are" else "de_flu_status").copy()

s["name"] = s["state"].map(STATE_NAMES)
s["iso"] = "DE-" + s["state"]
s["level_key"] = s.apply(lambda r: r["level"] if r["fresh"] and r["level"] else "none", axis=1)
s["Level"] = s.apply(lambda r: level_label(r["level"], r["fresh"]), axis=1)
s["Trend"] = s.apply(lambda r: trend_label(r["trend"]) if r["fresh"] else "", axis=1)
states = s[s["state"] != "DE"]

cmap = {k: v for k, v in LEVEL_COLORS.items() if k} | {"none": LEVEL_COLORS[None]}
left, right = st.columns([1.3, 1], gap="medium")
with left:
    fig = px.choropleth(states, geojson=states_geojson(), locations="iso", featureidkey="properties.shapeISO",
                        color="level_key", color_discrete_map=cmap, labels={"Level": t("level", L), "Trend": t("trend", L), },
                     hover_name="name",
                        hover_data={"level_key": False, "iso": False, "Level": True, "Trend": True})
    fig.update_traces(marker_line_color="white", marker_line_width=1.5)
    fig.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
    fig.update_layout(height=phone_height(640, 430), margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    st.markdown(legend_html(), unsafe_allow_html=True)
    st.plotly_chart(polish(fig), width="stretch", config=PLOT_CONFIG, theme=None)

with right:
    opts = ["DE"] + sorted(states["state"], key=lambda k: STATE_NAMES[k])
    pick = st.selectbox(t("pick_state", L), opts,
                        format_func=lambda k: t("germany_whole", L) if k == "DE" else STATE_NAMES[k])
    row = s[s["state"] == pick].iloc[0].to_dict()
    place = t("ov_germany", L) if pick == "DE" else STATE_NAMES[pick]
    st.markdown(badge(row["level"], row["trend"], row["fresh"]), unsafe_allow_html=True)
    st.markdown(sentence(place, f"m_{measure}", row))
    st.caption(t("as_of", L).format(date=data_date(row["date"])))
    st.markdown(f"**{t('chart_title', L)}**")
    st.plotly_chart(polish(season_chart(series[series["state"] == pick], row, t("u_per100k", L))), width="stretch",
                    config=PLOT_CONFIG, theme=None)
    st.caption(t("bands_note", L))

with st.expander(t("show_table", L)):
    tab = add_keys(s).assign(order=lambda d: (d["state"] != "DE").astype(int)).sort_values(["order", "name"])
    tab["name"] = [t("germany_whole", L) if k == "DE" else n for k, n in zip(tab["state"], tab["name"])]
    show_table(tab, {"name": t("col_state", L), "Level": t("level", L),
                                                 "Trend": t("trend", L)})
