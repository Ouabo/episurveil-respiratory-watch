"""Overview: the few messages that matter this week, then the details pages."""
import pandas as pd
import streamlit as st

from fluwatch.build import STATE_NAMES
from fluwatch.i18n import t
from fluwatch.ui import (INK, LEVEL_COLORS, MUTED, TREND_COLORS, add_keys, badge, data_date, lang, legend_html,
                         level_label, load, meta, show_table, trend_label)

L = lang()
RANK = {"very_high": 3, "high": 2, "moderate": 1, "low": 0}

are_s, flu_s, eu_s, ww_s = load("de_are_status"), load("de_flu_status"), load("eu_status"), load("ww_status")
m = meta()

de = are_s[are_s["state"] == "DE"].iloc[0].to_dict()
fl = flu_s[flu_s["state"] == "DE"].iloc[0].to_dict()
fl_states = flu_s[(flu_s["state"] != "DE") & flu_s["fresh"]]
n_flu_rising = int((fl_states["trend"] == "rising").sum())
eu_f = eu_s[eu_s["fresh"]]
eu_above = eu_f[eu_f["level"].isin(["moderate", "high", "very_high"])]


# ---------- places to watch (all sources) ----------
def watch_rows():
    rows = []
    for r in eu_f.itertuples():
        rows.append((r.country, t("t_country", L), t(f"m_{r.measure}", L), r.level, r.trend, True))
    for src, key in ((are_s, "m_are"), (flu_s, "m_flu")):
        for r in src[(src["state"] != "DE") & src["fresh"]].itertuples():
            rows.append((STATE_NAMES[r.state], t("t_state", L), t(key, L), r.level, r.trend, True))
    for r in ww_s[ww_s["fresh"] & ~ww_s["not_detected"]].itertuples():
        rows.append((r.site, t("t_city", L), t(f"m_ww_{r.pathogen}", L), r.level, r.trend, True))
    d = pd.DataFrame(rows, columns=["place", "type", "what", "level", "trend", "fresh"])
    d = d[d["level"].isin(["high", "very_high"]) | ((d["level"] == "moderate") & (d["trend"] == "rising"))]
    d = d.assign(rank=d["level"].map(RANK), up=(d["trend"] == "rising").astype(int))
    return d.sort_values(["rank", "up", "place"], ascending=[False, False, True])


watch = watch_rows()

# ---------- header ----------
st.title(t("app_title", L))
st.markdown(f"<p style='font-size:1.2rem;color:#374151;margin-top:-6px'>{t('tagline', L)}</p>",
            unsafe_allow_html=True)

# ---------- 1. the headline box ----------
def city_of(site, all_sites):
    """'Berlin Ruhleben' -> 'Berlin' when several plants share the first word."""
    for sep in (" ", "-"):
        head = site.split(sep)[0]
        if head != site and sum(x.startswith(head + sep) for x in all_sites) >= 2:
            return head
    return site


def high_places(w):
    sites = list(ww_s["site"].unique())
    hi = w[w["level"].isin(["high", "very_high"])].assign(rank=lambda d: d["level"].map(RANK))
    hi = hi.sort_values(["rank", "population"], ascending=False)
    return list(dict.fromkeys(city_of(x, sites) for x in hi["site"]))


lines = [t("head_de", L).format(level=t(de["level"], L).lower() if de["level"] else "-",
                                trend=t(de["trend"], L).lower() if de["trend"] else "-")]
flu_line = t("head_flu", L).format(n=n_flu_rising, m=len(fl_states)) if n_flu_rising else t("head_flu_none", L)
flu_hi = high_places(ww_s[(ww_s["pathogen"] == "flu") & ww_s["fresh"] & ~ww_s["not_detected"]])
if flu_hi:
    flu_line += t("head_flu_ww", L).format(places=", ".join(flu_hi[:3]))
lines.append(flu_line)
for v in ("covid", "rsv"):
    w = ww_s[(ww_s["pathogen"] == v) & ww_s["fresh"]]
    nr = int((w["trend"] == "rising").sum())
    if nr >= max(3, 0.2 * len(w)):
        line = t("head_ww", L).format(virus=t(f"V_{v}", L), n=nr, m=len(w))
        hp = high_places(w[~w["not_detected"]])
        if hp:
            line += t("head_ww_high", L).format(places=", ".join(hp[:4]))
        lines.append(line + ".")
if len(eu_above):
    names = ", ".join(eu_above.sort_values("level", key=lambda x: x.map(RANK), ascending=False)["country"].head(5))
    lines.append(t("head_eu", L).format(n=len(eu_above), m=len(eu_f), names=names))
else:
    lines.append(t("head_eu_none", L))
worst = max([RANK.get(de["level"], 0)] + list(watch["rank"]) + [0])
accent = LEVEL_COLORS[[k for k, v in RANK.items() if v == worst][0]] if worst else "#F2A65A"

import re  # noqa: E402

BOLD = re.compile(r"[*][*](.+?)[*][*]")
html_lines = "".join("<li style='margin:4px 0'>" + BOLD.sub(r"<b>\1</b>", x) + "</li>" for x in lines)
st.markdown(
    f"<div style='background:#FFF8F1;border-left:8px solid {accent};border-radius:10px;padding:18px 22px;margin:8px 0 18px'>"
    f"<div style='font-size:0.95rem;letter-spacing:.04em;text-transform:uppercase;color:{MUTED};font-weight:700'>"
    f"{t('glance', L)} · {t('as_of', L).format(date=data_date(de['date']))}</div>"
    f"<ul style='font-size:1.3rem;line-height:1.5;color:{INK};margin:10px 0 0;padding-left:1.2rem'>{html_lines}</ul></div>",
    unsafe_allow_html=True)


# ---------- 2. four key numbers ----------
def card(title, big, line, extra="", top=None):
    return (f"<div style='border:1px solid #E5E7EB;border-top:6px solid {top or '#E5E7EB'};border-radius:10px;"
            f"padding:14px 16px;height:100%'>"
            f"<div style='font-weight:700;font-size:1.05rem;color:{INK}'>{title}</div>"
            f"<div style='font-size:2.6rem;font-weight:800;line-height:1.15;color:{INK};margin:6px 0 2px'>{big}</div>"
            f"<div style='font-size:1rem;color:{INK}'>{line}</div>{extra}</div>")


c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown(card(t("kp_doctor", L), level_label(de["level"], de["fresh"]), trend_label(de["trend"]),
                     top=LEVEL_COLORS[de["level"]]), unsafe_allow_html=True)
    st.page_link("views/germany.py", label=f"{t('more', L)} →")
with c2:
    st.markdown(card(t("kp_flu", L), f"{n_flu_rising} / {len(fl_states)}", t("kp_flu_line", L),
                     f"<div style='margin-top:8px'>{badge(fl['level'], fl['trend'], fl['fresh'])}</div>",
                     top=TREND_COLORS["rising"] if n_flu_rising >= len(fl_states) / 2 else LEVEL_COLORS[fl["level"]]),
                unsafe_allow_html=True)
    st.page_link("views/germany.py", label=f"{t('more', L)} →")
with c3:
    names = ", ".join(eu_above.sort_values("level", key=lambda s: s.map(RANK), ascending=False)["country"].head(5))
    st.markdown(card(t("kp_eu", L), f"{len(eu_above)} / {len(eu_f)}", t("kp_eu_line", L),
                     f"<div style='color:{MUTED};margin-top:6px;font-size:0.95rem'>{names}</div>"
                     f"<div style='margin-top:4px;font-size:0.95rem'>{t('kp_eu_rising', L).format(n=int((eu_f['trend'] == 'rising').sum()))}</div>",
                     top=LEVEL_COLORS["moderate"] if len(eu_above) else LEVEL_COLORS["low"]), unsafe_allow_html=True)
    st.page_link("views/europe.py", label=f"{t('more', L)} →")
st.markdown(f"<div style='font-weight:700;font-size:1.15rem;margin:18px 0 6px;color:{INK}'>{t('kp_ww', L)} "
            f"<span style='font-weight:400;font-size:0.95rem;color:{MUTED}'>· {t('as_of_day', L).format(date=data_date(m['ww_latest_date']))}</span></div>",
            unsafe_allow_html=True)
v1, v2, v3 = st.columns(3, gap="medium")
for col, v in zip((v1, v2, v3), ("flu", "rsv", "covid")):
    w = ww_s[(ww_s["pathogen"] == v) & ww_s["fresh"]]
    nr, nd = int((w["trend"] == "rising").sum()), int(w["not_detected"].sum())
    colr = TREND_COLORS["rising"] if nr else MUTED
    with col:
        st.markdown(card(t(f"v_{v}", L), f"<span style='color:{colr}'>↑ {nr}</span> / {len(w)}",
                         t("kp_ww_rising", L).format(n=nr, m=len(w)),
                         f"<div style='color:{MUTED};margin-top:6px;font-size:0.95rem'>{t('kp_ww_nd', L).format(n=nd, m=len(w))}</div>",
                         top=TREND_COLORS["rising"] if nr >= 0.2 * max(len(w), 1) else "#9CA3AF"), unsafe_allow_html=True)
st.page_link("views/city.py", label=f"{t('nav_city', L)} →")

# ---------- 3. places to watch ----------
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
st.subheader(t("watch_title", L))
st.caption(t("watch_intro", L))
if len(watch):
    tab = add_keys(watch)
    tab["Level"] = [level_label(x) for x in tab["level"]]
    tab["Trend"] = [trend_label(x) for x in tab["trend"]]
    show_table(tab.head(12), {"place": t("col_place", L), "type": "", "what": t("col_what", L),
                              "Level": t("level", L), "Trend": t("trend", L)}, hide_on_phone=("type",))
else:
    st.success(t("head_calm", L))

# ---------- 4. how to read ----------
with st.expander(t("how_to_read", L)):
    st.markdown(t("how_to_read_body", L))
    st.markdown(legend_html(), unsafe_allow_html=True)
    st.markdown(t("level_help", L))
    st.markdown(t("trend_help", L))
