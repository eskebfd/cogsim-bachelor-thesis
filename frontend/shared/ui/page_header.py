from html import escape

import streamlit as st


def render_page_header(
    title: str,
    subtitle: str,
    *,
    icon: str = "circle",
) -> None:
    subtitle_markup = (
        f'<div class="cogsim-page-subtitle">{escape(subtitle)}</div>'
        if subtitle
        else ""
    )
    st.markdown(
        f"""
        <div class="cogsim-page-header">
            <h1 class="cogsim-page-title">{escape(title)}</h1>
            {subtitle_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )
