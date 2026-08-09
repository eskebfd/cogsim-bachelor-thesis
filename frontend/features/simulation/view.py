import streamlit as st

from frontend.features.simulation.results import render_simulation_results
from frontend.shared.ui.loading_overlay import clear_stale_global_loading_overlay
from frontend.shared.ui.status_messages import render_info_message
from frontend.shared.ui.page_header import render_page_header


def render_results_view():
    clear_stale_global_loading_overlay()
    render_page_header(
        "Ergebnisse",
        "",
        icon="bar-chart-3",
    )
    with st.container(border=True):
        simulation_result = st.session_state.get("simulation_result")

        if simulation_result:
            render_simulation_results(simulation_result)
        else:
            render_info_message("Es liegen noch keine Ergebnisse vor.")
