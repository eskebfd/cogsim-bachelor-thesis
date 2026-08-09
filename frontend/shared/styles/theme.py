import streamlit as st

from frontend.shared.styles.loader import build_cogsim_css


def inject_cogsim_theme() -> None:
    st.markdown(
        build_cogsim_css(),
        unsafe_allow_html=True,
    )
