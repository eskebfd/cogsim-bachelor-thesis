import streamlit as st

from frontend.shared.ui.status_messages import render_info_message
from frontend.workflow.steps import SIMULATION_FOUNDATIONS_STEP


def request_simulation_preparation() -> None:
    st.session_state["pending_simulation_preparation"] = True


def render_base_review_actions() -> None:
    base_model_preview = st.session_state.get("base_model_preview")

    if not base_model_preview:
        return

    if st.session_state.get("computed_parameters_preview"):
        render_info_message(
            "Der Simulationsplan wurde bereits vorbereitet."
        )

        st.button(
            "Simulationsplan erneut vorbereiten",
            type="primary",
            use_container_width=True,
            on_click=request_simulation_preparation,
        )

        return

    st.button(
        "Simulationsplan vorbereiten",
        type="primary",
        use_container_width=True,
        on_click=request_simulation_preparation,
    )


def render_review_action_panel(current_step: int) -> None:
    if current_step == SIMULATION_FOUNDATIONS_STEP:
        st.write("")
        with st.container(border=True):
            render_base_review_actions()
