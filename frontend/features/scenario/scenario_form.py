import streamlit as st
from html import escape

from frontend.features.scenario.screenshot_tool import (
    apply_pending_screenshot_task_text,
    _render_task_screenshot_attachment,
)
from frontend.shared.ui.icons import render_icon


def _dynamic_text_area_height(
    text: str,
    *,
    min_height: int,
    max_height: int,
    wrap_at: int,
    base_height: int = 92,
) -> int:
    lines = max(1, text.count("\n") + 1)
    wrapped_lines = max(0, len(text) // wrap_at)

    return max(
        min_height,
        min(
            max_height,
            base_height + (lines + wrapped_lines) * 22,
        ),
    )


def _dynamic_task_text_area_height(task_text: str) -> int:
    return _dynamic_text_area_height(
        task_text,
        min_height=120,
        max_height=360,
        wrap_at=115,
        base_height=58,
    )


def _render_section_header(
    icon: str,
    title: str,
    description: str,
) -> None:
    header_html = (
        '<div class="cogsim-scenario-section-header">'
        '<div class="cogsim-scenario-section-icon">'
        f"{render_icon(icon, size=20, stroke_width=1.8)}"
        "</div>"
        '<div class="cogsim-scenario-section-copy">'
        f'<div class="cogsim-scenario-section-title">{title}</div>'
        '<div class="cogsim-scenario-section-description">'
        f"{description}"
        "</div>"
        "</div>"
        "</div>"
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True,
    )


def _render_field_heading(
    *,
    icon: str,
    title: str,
    description: str,
) -> None:
    st.markdown(
        (
            '<div class="cogsim-scenario-field-heading">'
            '<div class="cogsim-scenario-field-heading__icon">'
            f"{render_icon(icon, size=18, stroke_width=1.9)}"
            "</div>"
            '<div class="cogsim-scenario-field-heading__copy">'
            '<div class="cogsim-scenario-field-heading__title">'
            f"{escape(title)}"
            "</div>"
            '<div class="cogsim-scenario-field-heading__description">'
            f"{escape(description)}"
            "</div>"
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def build_scenario_description(
    task_text: str | None = None,
    interface_text: str | None = None,
    environment_text: str | None = None,
) -> str:
    task = (
        st.session_state.get("scenario_task", "")
        if task_text is None
        else task_text
    )
    interface = (
        st.session_state.get("scenario_interface", "")
        if interface_text is None
        else interface_text
    )
    environment = (
        st.session_state.get("scenario_environment", "")
        if environment_text is None
        else environment_text
    )

    return (
        f"Aufgabe\n{task.strip()}\n\n"
        f"Interface\n{interface.strip()}\n\n"
        f"Umgebung\n{environment.strip()}"
    )


def _render_scenario_text_input() -> str:
    apply_pending_screenshot_task_text()

    current_task_text = st.session_state.get("scenario_task", "")

    _render_field_heading(
        icon="target",
        title="Aufgabe",
        description="Was soll die Person am Ende geschafft haben?",
    )

    task_text = st.text_area(
        "Aufgabe",
        value=current_task_text,
        height=_dynamic_task_text_area_height(current_task_text),
        placeholder=(
            "Beschreibe das Ziel der Person und die wichtigsten Schritte, "
            "die dafür wahrscheinlich nötig sind."
        ),
        key="scenario_task",
        label_visibility="collapsed",
    )

    _render_task_screenshot_attachment()

    interface_column, environment_column = st.columns(
        2,
        gap="large",
    )

    with interface_column:
        current_interface_text = st.session_state.get("scenario_interface", "")
        _render_field_heading(
            icon="boxes",
            title="Interface",
            description="Welche Inhalte und Bedienelemente sieht die Person?",
        )
        interface_text = st.text_area(
            "Interface",
            value=current_interface_text,
            height=_dynamic_text_area_height(
                current_interface_text,
                min_height=135,
                max_height=520,
                wrap_at=58,
            ),
            placeholder=(
                "Was sieht die Person? Welche Inhalte, Buttons, Felder oder "
                "Navigationsbereiche sind wichtig?"
            ),
            key="scenario_interface",
            label_visibility="collapsed",
        )

    with environment_column:
        current_environment_text = st.session_state.get("scenario_environment", "")
        _render_field_heading(
            icon="activity",
            title="Umgebung",
            description="Welche äußeren Bedingungen beeinflussen die Nutzung?",
        )
        environment_text = st.text_area(
            "Umgebung",
            value=current_environment_text,
            height=_dynamic_text_area_height(
                current_environment_text,
                min_height=125,
                max_height=420,
                wrap_at=58,
            ),
            placeholder=(
                "In welcher Situation wird die Aufgabe erledigt? Gibt es "
                "Ablenkung, Zeitdruck oder besondere Bedingungen?"
            ),
            key="scenario_environment",
            label_visibility="collapsed",
        )

    scenario_description = build_scenario_description(
        task_text,
        interface_text,
        environment_text,
    )

    st.session_state.scenario_input = scenario_description

    return scenario_description
