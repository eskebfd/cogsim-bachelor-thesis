import streamlit as st

from frontend.shared.styles.theme import inject_cogsim_theme
from frontend.state import init_state
from frontend.features.home.view import render_home_view
from frontend.workflow.view import render_workflow_view
from frontend.shared.ui.sidebar import render_sidebar
from frontend.shared.ui.scroll_position import render_scroll_to_top_on_page_change

st.set_page_config(
    page_title="CogSim",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_cogsim_theme()

init_state()

render_sidebar()

render_scroll_to_top_on_page_change(
    f"{st.session_state.current_view}:{st.session_state.get('simulation_step', 1)}"
)

if st.session_state.current_view == "home":
    render_home_view()

elif st.session_state.current_view == "simulation":
    render_workflow_view()
