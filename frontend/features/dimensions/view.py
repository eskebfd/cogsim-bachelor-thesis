import streamlit as st

from frontend.features.dimensions.section import (
    build_detected_scenario_context,
    render_dimensions_section,
)
from frontend.features.evaluation_goals.actions import (
    generate_base_models_with_progress,
)
from frontend.shared.ui.page_header import (
    render_page_header,
)
from frontend.shared.ui.status_messages import (
    render_info_message,
    render_warning_message,
)
from frontend.workflow.actions import (
    clear_model_outputs,
    go_to_step,
    update_modeling_setup_state,
)
from frontend.state import (
    apply_dimension_values_to_model_previews,
)

DIMENSION_FOCUS_LABELS = {
    "task": "Aufgabe",
    "interface": "Interface",
    "environment": "Umgebung",
}


def render_scenario_setup_view() -> None:
    render_page_header(
        "Anforderungen",
        "",
        icon="sliders-horizontal",
    )

    scenario_description = st.session_state.get("scenario_input")
    dimensions = st.session_state.get("dimensions")

    if not scenario_description:
        render_warning_message("Es wurde noch kein Szenario angegeben.")
        return

    if not dimensions:
        render_info_message("Es wurden noch keine Szenariowerte erkannt.")
        return

    focus_area = st.session_state.get("dimension_focus_area")
    if focus_area in DIMENSION_FOCUS_LABELS:
        render_info_message(
            (
                "Passe hier gezielt die Werte für "
                f"{DIMENSION_FOCUS_LABELS[focus_area]} an."
            )
        )

    st.session_state.dimensions = render_dimensions_section(dimensions)

    detected = build_detected_scenario_context(dimensions)

    st.session_state.device = detected["device"]
    st.session_state.detected_task = detected["task"]
    st.session_state.environment = detected["environment"]

    update_modeling_setup_state(
        scenario_description,
        st.session_state.dimensions,
    )

    st.write("")

    if st.button(
        "Weiter zu den Simulationsgrundlagen",
        type="primary",
        use_container_width=True,
    ):
        if st.session_state.get("return_to_models_after_dimension_edit"):
            apply_dimension_values_to_model_previews(
                st.session_state.dimensions,
            )
            st.session_state.dimension_focus_area = None
            st.session_state.return_to_models_after_dimension_edit = False
            go_to_step(6)
            return

        st.session_state.dimension_focus_area = None
        st.session_state.return_to_models_after_dimension_edit = False

        base_model_preview = st.session_state.get("base_model_preview") or {}
        has_complete_model_preview = all(
            base_model_preview.get(key)
            for key in (
                "task_model",
                "interface_model",
                "environment_model",
                "user_model",
            )
        )

        if has_complete_model_preview:
            apply_dimension_values_to_model_previews(
                st.session_state.dimensions,
            )
            go_to_step(6)
            return

        task_flow_model = (st.session_state.get("base_model_preview") or {}).get(
            "task_model",
            {},
        )
        clear_model_outputs()
        if task_flow_model:
            st.session_state.base_model_preview = {
                "task_model": task_flow_model,
            }

        if generate_base_models_with_progress(scenario_description):
            go_to_step(6)
