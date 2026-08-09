import streamlit as st

from frontend.features.models.actions import (
    add_missing_task_step,
)
from frontend.features.models.task_flow_summary import (
    render_task_structure_review,
)
from frontend.shared.ui.loading_overlay import global_loading
from frontend.shared.ui.page_header import render_page_header
from frontend.shared.ui.status_messages import (
    render_warning_message,
)
from frontend.workflow.actions import analyze_scenario_dimensions, go_to_step


def render_task_flow_view() -> None:
    render_page_header(
        "Aufgabenablauf",
        "",
        icon="list-checks",
    )

    base_model_preview = st.session_state.get("base_model_preview") or {}
    task_model = base_model_preview.get("task_model") or {}

    if not task_model:
        render_warning_message(
            "Es wurde noch kein Aufgabenablauf erkannt. "
            "Gehe zurück zum Szenario und starte die Analyse erneut."
        )
        return

    st.markdown(
        (
            '<div class="cogsim-task-flow-intro">'
            '<div class="cogsim-task-flow-intro__title">'
            "Erkannten Aufgabenablauf prüfen"
            "</div>"
            '<div class="cogsim-task-flow-intro__text">'
            "Hier siehst du, wie CogSim die Aufgabe verstanden hat. Prüfe, "
            "ob die Reihenfolge ungefähr zum echten Ablauf passt, und ergänze "
            "fehlende Schritte direkt hier."
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    task_review = render_task_structure_review(task_model)
    missing_step_request = task_review.get("missing_step_request")

    if missing_step_request:
        with global_loading(
            "Das Feedback zum Aufgabenablauf wird geprüft.",
            hint="Der beschriebene Hinweis wird in den bestehenden Ablauf eingeordnet.",
            estimated_seconds=28.0,
        ):
            add_missing_task_step(missing_step_request)

        return

    st.write("")

    if st.button(
        "Anforderungen erstellen",
        type="primary",
        use_container_width=True,
    ):
        scenario_description = st.session_state.get("scenario_input", "")
        scenario_image = st.session_state.get("scenario_image_upload")
        with global_loading(
            "Die Anforderungen werden erstellt.",
            hint="Aus dem geprüften Ablauf werden einschätzbare Anforderungen abgeleitet.",
            estimated_seconds=35.0,
        ):
            analyze_scenario_dimensions(
                scenario_description,
                scenario_image=scenario_image,
            )
        go_to_step(5)
