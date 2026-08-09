import streamlit as st
from html import escape

from frontend.workflow.steps import WORKFLOW_STEPS


def _step_state(
    step_number: int,
    current_step: int,
) -> str:
    if step_number == current_step:
        return "active"

    if step_number < current_step:
        return "completed"

    return "upcoming"


def render_step_navigation() -> None:
    current_step = st.session_state.get(
        "simulation_step",
        1,
    )

    steps_html = "".join(
        (
            f'<div class="cogsim-timeline-step is-{_step_state(step_number, current_step)}">'
            '<div class="cogsim-timeline-point">'
            f"{step_number}"
            "</div>"
            '<div class="cogsim-timeline-label">'
            f"{escape(label)}"
            "</div>"
            "</div>"
        )
        for step_number, label in WORKFLOW_STEPS
    )

    st.html(
        (
            '<div class="st-key-workflow_stepper_v7">'
            '<div class="cogsim-workflow-timeline">'
            f"{steps_html}"
            "</div>"
            "</div>"
        )
    )
