import streamlit as st

from frontend.features.scenario.input_section import (
    render_multimodal_summary,
    render_scenario_input_section,
)
from frontend.shared.ui.page_header import render_page_header
from frontend.state import (
    get_session_id,
    reset_generated_data,
    update_backend_state,
)
from frontend.features.task_flow.actions import generate_task_flow_with_progress
from frontend.workflow.actions import (
    go_to_step,
)


def has_scenario_text_input() -> bool:
    return any(
        str(st.session_state.get(key, "")).strip()
        for key in (
            "scenario_task",
            "scenario_interface",
            "scenario_environment",
        )
    )


def render_scenario_input_view() -> None:
    render_page_header(
        "Szenario",
        "",
        icon="file-text",
    )

    old_input = st.session_state.get(
        "scenario_input",
        "",
    )

    scenario_description = render_scenario_input_section()

    scenario_image = st.session_state.get("scenario_image_upload")

    if scenario_description != old_input:
        reset_generated_data(preserve_profiles=True, preserve_evaluation=True)

        st.session_state.scenario_image_upload = scenario_image

    update_backend_state(
        scenario_description=scenario_description,
        scenario_text=scenario_description,
        scenario_image=scenario_image,
        session_id=get_session_id(),
    )

    st.write("")

    if st.button(
        "Aufgabenablauf erstellen",
        type="primary",
        use_container_width=True,
    ):
        has_description = has_scenario_text_input()

        has_image = scenario_image is not None

        if not has_description and not has_image:
            st.error(
                "Bitte beschreibe kurz die Aufgabe oder lade einen Screenshot hoch."
            )
            return

        if not has_description and has_image:
            st.warning(
                "Der Screenshot hilft beim Erkennen möglicher Arbeitsschritte. "
                "Noch besser wird die Analyse, wenn du zusätzlich kurz erklärst, "
                "was die Person erreichen möchte."
            )

        reset_generated_data(preserve_profiles=True, preserve_evaluation=True)

        st.session_state.scenario_image_upload = scenario_image

        if generate_task_flow_with_progress(scenario_description):
            go_to_step(4)

    render_multimodal_summary(st.session_state.get("multimodal_analysis"))
