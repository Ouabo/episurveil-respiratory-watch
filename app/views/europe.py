import plotly.express as px
import streamlit as st

from fluwatch.i18n import t
from fluwatch.ui import polish, LEVEL_COLORS, add_keys, show_table, badge, data_date, lang, legend_html, level_label, load, season_chart, sentence, trend_label

L = lang()
st.title(t("eu_title", L))
st.caption(t("eu_intro", L))

eu = load("eu")
s = load("eu_status").copy()
s["level_key"] = s.apply(lambda r: r["level"] if r["fresh"] and r["level"] else "none", axis=1)
s["Level"] = s.apply(lambda r: level_label(r["level"], r["fresh"]), axis=1)
s["Trend"] = s.apply(lambda r: trend_label(r["trend"]) if r["fresh"] else "", axis=1)
s["Measure"] = s["measure"].map(lambda k: t(f"m_{k}", L))
s["Week"] = s["date"].map(data_date)

ISO3 = {"Austria": "AUT", "Belgium": "BEL", "Bulgaria": "BGR", "Croatia": "HRV", "Cyprus": "CYP", "Czechia": "CZE",
        "Denmark": "DNK", "Estonia": "EST", "Finland": "FIN", "France": "FRA", "Germany": "DEU", "Greece": "GRC",
        "Hungary": "HUN", "Iceland": "ISL", "Ireland": "IRL", "Italy": "ITA", "Latvia": "LVA", "Lithuania": "LTU",
        "Luxembourg": "LUX", "Malta": "MLT", "Netherlands": "NLD", "Norway": "NOR", "Poland": "POL",
        "Portugal": "PRT", "Romania": "ROU", "Slovakia": "SVK", "Slovenia": "SVN", "Spain": "ESP", "Sweden": "SWE",
        "Liechtenstein": "LIE"}
s["iso3"] = s["country"].map(ISO3)
cmap = {k: v for k, v in LEVEL_COLORS.items() if k} | {"none": LEVEL_COLORS[None]}
fig = px.choropleth(s.dropna(subset=["iso3"]), locations="iso3", locationmode="ISO-3", color="level_key",
                    color_discrete_map=cmap, labels={"Level": t("level", L), "Trend": t("trend", L), "Measure": t("col_measure", L), "Week": t("col_week", L), },
                     scope="europe",
                    hover_name="country", hover_data={"level_key": False, "Level": True, "Trend": True,
                                                       "Measure": True, "Week": True, "iso3": False})
fig.update_traces(marker_line_color="white", marker_line_width=1)
fig.update_geos(showcountries=True, countrycolor="#FFFFFF", showland=True, landcolor="#F3F4F6",
                showframe=False, projection_type="natural earth", lataxis_range=[34, 71], lonaxis_range=[-25, 40])
fig.update_layout(height=560, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
st.markdown(legend_html(), unsafe_allow_html=True)
st.plotly_chart(polish(fig), width="stretch", config={"displayModeBar": False}, theme=None)

countries = sorted(s["country"])
default = countries.index("Germany") if "Germany" in countries else 0
country = st.selectbox(t("pick_country", L), countries, index=default)
row = s[s["country"] == country].iloc[0].to_dict()
st.markdown(badge(row["level"], row["trend"], row["fresh"]), unsafe_allow_html=True)
st.markdown(sentence(country, f"m_{row['measure']}", row))
st.caption(t("as_of", L).format(date=data_date(row["date"])))
st.markdown(f"**{t('chart_title', L)}**")
unit = t("u_per100k", L)
st.plotly_chart(polish(season_chart(eu[eu["country"] == country], row, unit)), width="stretch",
                config={"displayModeBar": False}, theme=None)
st.caption(t("bands_note", L))

with st.expander(t("show_table", L)):
    show_table(add_keys(s).sort_values("country"), {
        "country": t("col_country", L), "Level": t("level", L), "Trend": t("trend", L),
        "Measure": t("col_measure", L), "Week": t("col_week", L)})
