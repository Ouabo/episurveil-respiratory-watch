from pathlib import Path

import streamlit as st

from fluwatch.i18n import t
from fluwatch.sources import GEO_SOURCES, SOURCES
from fluwatch.ui import lang, meta

L = lang()
st.title(t("about_title", L))
st.info(t("disclaimer", L))

st.subheader(t("how_decided", L))
st.markdown(t("how_decided_body", L))

st.subheader(t("sources", L))
for v in SOURCES.values():
    st.markdown(f"- [{v['name']}]({v['home']}) · {v['licence']}")
for v in GEO_SOURCES.values():
    st.markdown(f"- {v}")

st.subheader(t("share_title", L))
st.markdown(t("share_body", L))
st.code("https://episurveil-respiratory.streamlit.app/", language=None, wrap_lines=True)
st.image(str(Path(__file__).resolve().parents[1] / "assets" / "qr_respiratory_watch.png"), width=220)

m = meta()
st.caption(f"{t('updated', L)}: {m['built_utc']} UTC")
st.caption(t("author", L))
