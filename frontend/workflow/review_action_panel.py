import streamlit as st

from frontend.shared.ui.loading_overlay import global_loading
from frontend.shared.ui.status_messages import render_info_message
from frontend.features.models.actions import prepare_simulation
from frontend.workflow.steps import SIMULATION_FOUNDATIONS_STEP


def render_base_review_actions() -> None:
    base_model_preview = st.session_state.get("base_model_preview")

    if not base_model_preview:
        return

    if st.session_state.get("computed_parameters_preview"):
        render_info_message(
            "Der Simulationsplan wurde bereits vorbereitet."
        )

        if st.button(
            "Simulationsplan erneut vorbereiten",
            type="primary",
            use_container_width=True,
        ):
            with global_loading(
                "Der Simulationsplan wird vorbereitet.",
                hint="Die aktuell geprüften Werte werden übernommen.",
                estimated_seconds=18.0,
            ):
                prepare_simulation()

        return

    if st.button(
        "Simulationsplan vorbereiten",
        type="primary",
        use_container_width=True,
    ):
        with global_loading(
            "Der Simulationsplan wird vorbereitet.",
            hint="Die aktuell geprüften Werte werden übernommen.",
            estimated_seconds=18.0,
        ):
            prepare_simulation()


def render_review_action_panel(current_step: int) -> None:
    if current_step == SIMULATION_FOUNDATIONS_STEP:
        st.write("")
        with st.container(border=True):
            render_base_review_actions()
