"""EpiSurveil Respiratory Watch - entry point. Run: streamlit run app/Home.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st  # noqa: E402

from fluwatch.i18n import t  # noqa: E402

st.set_page_config(page_title="EpiSurveil Respiratory Watch", page_icon="🌡️", layout="wide")

# larger, easier-to-read text everywhere (Streamlit sizes are in rem, so this scales the whole app)
st.markdown("""<style>
html { font-size: 20px; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { font-size: 1.05rem; line-height: 1.55; }
[data-testid="stCaptionContainer"] p { font-size: 0.95rem; }
[data-testid="stSidebarNav"] span { font-size: 1.05rem; }
.block-container, [data-testid="stMainBlockContainer"] { padding-left: 2rem; padding-right: 2rem; padding-top: 2.5rem; max-width: 1600px; }
</style>""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state["lang"] = "de" if st.query_params.get("lang") == "de" else "en"
with st.sidebar:
    choice = st.radio("Language / Sprache", ["English", "Deutsch"], horizontal=True,
                      index=1 if st.session_state["lang"] == "de" else 0)
    st.session_state["lang"] = "de" if choice == "Deutsch" else "en"
L = st.session_state["lang"]

V = Path(__file__).parent / "views"
pages = [
    st.Page(V / "overview.py", title=t("nav_home", L), icon=":material/home:", default=True),
    st.Page(V / "europe.py", title=t("nav_europe", L), icon=":material/public:", url_path="europe"),
    st.Page(V / "germany.py", title=t("nav_germany", L), icon=":material/map:", url_path="germany"),
    st.Page(V / "city.py", title=t("nav_city", L), icon=":material/water_drop:", url_path="city"),
    st.Page(V / "about.py", title=t("nav_about", L), icon=":material/info:", url_path="about"),
]
st.navigation(pages).run()

with st.sidebar:
    st.caption(t("disclaimer", L))
