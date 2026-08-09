import streamlit as st

from frontend.workflow.actions import go_home
from frontend.shared.ui.icons import render_icon


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            f"""
            <div class="cogsim-sidebar-section">
                <div class="cogsim-sidebar-title">
                    {render_icon("home", size=16)}
                    <span>Navigation</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Startseite",
            key="sidebar_home",
            use_container_width=True,
        ):
            go_home()
