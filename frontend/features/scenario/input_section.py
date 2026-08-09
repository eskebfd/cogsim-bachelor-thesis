import streamlit as st

from frontend.features.scenario.scenario_form import (
    _render_section_header,
    _render_scenario_text_input,
)


def render_multimodal_summary(
    multimodal_analysis: dict | None,
) -> None:
    if not multimodal_analysis:
        return

    sections = [
        ("Aus dem Text erkannt", "text_signals"),
        ("Aus dem Bild erkannt", "image_signals"),
        ("Durch beide Quellen bestätigt", "confirmed_signals"),
        ("Noch unklar", "missing_information"),
        ("Widersprüche", "conflicts"),
    ]

    with st.expander(
        "Erkannte Informationen anzeigen",
        expanded=False,
    ):
        for label, key in sections:
            values = multimodal_analysis.get(key) or []

            if not values:
                continue

            st.markdown(f"**{label}**")

            for value in values:
                st.markdown(f"- {value}")

        warning = multimodal_analysis.get("image_analysis_warning")

        if warning:
            st.warning(warning)


def render_scenario_input_section() -> str:
    _render_section_header(
        icon="file-text",
        title="Szenario beschreiben",
        description=(
            "Halte fest, was die Person tun möchte, was sie dabei sieht "
            "und unter welchen Bedingungen sie die Aufgabe erledigt."
        ),
    )

    with st.container(key="scenario_text_panel"):
        scenario_description = _render_scenario_text_input()

    st.session_state.scenario_input = scenario_description

    return scenario_description
