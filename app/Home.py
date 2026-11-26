"""EpiSurveil Respiratory Watch - entry point. Run: streamlit run app/Home.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st  # noqa: E402

from fluwatch.i18n import t  # noqa: E402

st.set_page_config(page_title="EpiSurveil Respiratory Watch", page_icon="🌡️", layout="wide",
                   initial_sidebar_state="collapsed")

# larger, easier-to-read text everywhere (Streamlit sizes are in rem, so this scales the whole app);
# on phones (narrow screens) slightly smaller text, smaller titles and narrow side margins
st.markdown("""<style>
html { font-size: 20px; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { font-size: 1.05rem; line-height: 1.55; }
[data-testid="stCaptionContainer"] p { font-size: 0.95rem; }
.block-container, [data-testid="stMainBlockContainer"] { padding-left: 2rem; padding-right: 2rem; padding-top: 2.5rem; max-width: 1600px; }
@media (max-width: 640px) {
  html { font-size: 17px; }
  h1 { font-size: 1.75rem !important; line-height: 1.2 !important; }
  h2, h3 { font-size: 1.3rem !important; }
  .block-container, [data-testid="stMainBlockContainer"] { padding-left: 0.9rem; padding-right: 0.9rem; padding-top: 3.2rem; }
  [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { font-size: 1rem; line-height: 1.45; }
}
</style>""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state["lang"] = "de" if st.query_params.get("lang") == "de" else "en"

# page menu and language switch at the top of every page (the side menu is hard to find on phones);
# side by side on wide screens, stacked on phones
menu_col, lang_col = st.columns([4, 1.4], vertical_alignment="center")
with lang_col:
    choice = st.segmented_control("Language / Sprache", ["English", "Deutsch"], label_visibility="collapsed",
                                  default="Deutsch" if st.session_state["lang"] == "de" else "English")
    if choice:
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
# page menu as a row of buttons on every page: it wraps on phones, where Streamlit would hide its own menu
nav = st.navigation(pages, position="hidden")
labels = [p.title for p in pages]
cur = next((i for i, p in enumerate(pages) if p.url_path == nav.url_path), 0)
with menu_col:
    sel = st.pills("Menu", labels, default=labels[cur], label_visibility="collapsed", key=f"menu_{cur}_{L}")
if sel and sel != labels[cur]:
    st.switch_page(pages[labels.index(sel)])
nav.run()

st.divider()
st.caption(t("disclaimer", L))
