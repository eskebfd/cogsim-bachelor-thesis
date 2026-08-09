from html import escape

import streamlit as st

from frontend.features.computed_parameters.simulation_plan_review import (
    render_simulation_plan_review,
)
from frontend.features.simulation.actions import run_simulation_from_plan
from frontend.shared.ui.loading_overlay import global_loading
from frontend.shared.ui.page_header import render_page_header


COMPUTED_PARAMETER_LABELS = {
    "text_complexity": "Textschwierigkeit",
    "navigation_effort": "Navigationsaufwand",
    "decoding_load": "Dekodieraufwand",
    "visual_reading_load": "Visuelle Lesebelastung",
    "sustained_attention_load": "Daueraufmerksamkeitsbelastung",
    "inhibition_load": "Hemmungsbelastung",
    "attention_switching_load": "Belastung durch Aufgabenwechsel",
}

HIDDEN_COMPUTED_PARAMETERS = {
    "dyslexia_reading_load",
    "adhd_interaction_load",
}


def _computed_parameter_label(name: str) -> str:
    return COMPUTED_PARAMETER_LABELS.get(
        name,
        name.replace("_", " ").title(),
    )


def build_computed_parameter_rows(parameters: dict) -> list[dict]:
    return [
        {
            "Parameter": _computed_parameter_label(name),
            "Wert": value.get("value", value)
            if isinstance(value, dict)
            else value,
        }
        for name, value in parameters.items()
        if name != "assumptions" and name not in HIDDEN_COMPUTED_PARAMETERS
    ]


def _render_simulation_plan_intro() -> None:
    st.markdown(
        (
            '<div class="cogsim-plan-intro">'
            '<div class="cogsim-plan-intro__hint">'
            "Hinweis für die Testung: Dieser Schritt kann übersprungen werden. "
            "Er dient vor allem der Nachvollziehbarkeit in der Bachelorarbeit."
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _render_computed_parameter_cards(parameters: dict) -> None:
    parameter_rows = build_computed_parameter_rows(parameters)
    cards = []
    for row in parameter_rows:
        cards.append(
            (
                '<div class="cogsim-plan-value-card">'
                '<span class="cogsim-plan-value-card__label">'
                f"{escape(str(row['Parameter']))}"
                "</span>"
                '<span class="cogsim-plan-value-card__value">'
                f"{escape(str(row['Wert']))}"
                "</span>"
                "</div>"
            )
        )

    st.markdown(
        '<div class="cogsim-plan-value-grid">'
        + "".join(cards)
        + "</div>",
        unsafe_allow_html=True,
    )


def _request_simulation_run() -> None:
    st.session_state["pending_simulation_run"] = True


def _run_pending_simulation() -> None:
    with global_loading(
        "Die Simulation wird ausgeführt.",
        hint="Die ausgewählten Profile werden mit denselben Grundlagen verglichen.",
        min_visible_seconds=7.0,
        estimated_seconds=7.0,
    ):
        run_simulation_from_plan(rerun=False)
    st.rerun()


def render_simulation_plan_section() -> None:
    if st.session_state.pop("pending_simulation_run", False):
        _run_pending_simulation()
        return

    with st.container(key="simulation_plan_review"):
        backend_state = st.session_state.get("backend_state", {})
        simulation_plan = backend_state.get("simulation_plan")
        computed_parameters = backend_state.get("computed_parameters", {})

        _render_simulation_plan_intro()
        render_simulation_plan_review(simulation_plan or {})

        st.markdown(
            '<div class="cogsim-plan-section-title">Berechnete Planwerte</div>',
            unsafe_allow_html=True,
        )
        if computed_parameters:
            _render_computed_parameter_cards(computed_parameters)
        else:
            st.info("Es wurden noch keine Planwerte berechnet.")

        if computed_parameters:
            st.button(
                "Simulation starten",
                type="primary",
                use_container_width=True,
                on_click=_request_simulation_run,
            )


def render_simulation_plan_view() -> None:
    render_page_header(
        "Simulationsplan",
        "",
        icon="calculator",
    )
    render_simulation_plan_section()
