from html import escape

import streamlit as st

from frontend.shared.model_attribute_labels import (
    MODEL_ATTRIBUTE_LABELS,
)

SIGNAL_GROUPS = [
    ("task_signals", "Aufgabe"),
    ("interface_signals", "Interface"),
    ("environment_signals", "Umgebung"),
]

ATTRIBUTE_DEFINITIONS = {
    "task_complexity": "Wie anspruchsvoll die Aufgabe insgesamt ist.",
    "number_of_steps": "Wie viele größere Arbeitsschritte die Aufgabe wahrscheinlich hat.",
    "reading_demand": "Wie viel gelesen und verstanden werden muss.",
    "input_demand": "Wie viel die Person eingeben, auswählen oder bestätigen muss.",
    "memory_demand": "Wie viel sich die Person während der Aufgabe merken muss.",
    "unfamiliar_word_density": "Wie viele ungewohnte oder schwer einzuordnende Wörter vorkommen.",
    "orthographic_irregularity": "Wie stark Schreibweise und Worterkennung das Lesen erschweren können.",
    "morphological_complexity": "Wie komplex die Wortformen und zusammengesetzten Begriffe sind.",
    "sustained_attention_demand": "Wie lange die Person aufmerksam bei der Aufgabe bleiben muss.",
    "task_switching_demand": "Wie oft die Person zwischen Schritten oder Informationen wechseln muss.",
    "inhibition_demand": "Wie stark irrelevante Reize oder vorschnelle Handlungen ausgeblendet werden müssen.",
    "divided_attention_demand": "Wie stark mehrere Informationen gleichzeitig beachtet werden müssen.",
    "text_volume": "Wie viel Text auf der Oberfläche gelesen werden muss.",
    "sentence_length": "Wie lang und verschachtelt die Sätze wirken.",
    "word_difficulty": "Wie schwierig die verwendeten Wörter sind.",
    "technical_terms": "Wie viele Fachbegriffe oder spezielle Bezeichnungen vorkommen.",
    "visual_clutter": "Wie voll oder visuell unruhig die Oberfläche wirkt.",
    "navigation_complexity": "Wie schwer es ist, den richtigen Weg durch die Oberfläche zu finden.",
    "accessibility_support": "Wie gut die Oberfläche beim Verstehen und Bedienen unterstützt.",
    "feedback_quality": "Wie klar die Oberfläche Rückmeldungen, Fehler und Status anzeigt.",
    "text_legibility": "Wie gut lesbar der Text durch Größe, Kontrast und Darstellung ist.",
    "text_density": "Wie dicht Textinformationen auf engem Raum dargestellt werden.",
    "line_tracking_difficulty": "Wie schwer es ist, Zeilen und Textbereiche beim Lesen zu verfolgen.",
    "stimulus_density": "Wie viele Reize, Optionen oder Elemente gleichzeitig sichtbar sind.",
    "irrelevant_signal_load": "Wie viele ablenkende oder für die Aufgabe unwichtige Signale sichtbar sind.",
    "feedback_interruptiveness": "Wie stark Hinweise, Popups oder Rückmeldungen den Fokus unterbrechen.",
    "focus_guidance": "Wie gut die Oberfläche den Blick zum nächsten wichtigen Schritt führt.",
    "noise_level": "Wie laut oder störend die Umgebung wahrscheinlich ist.",
    "distractions": "Wie stark Unterbrechungen oder Ablenkungen die Aufgabe stören können.",
    "time_pressure": "Wie stark Zeitdruck die Bearbeitung beeinflusst.",
    "context_stability": "Wie stabil und vorhersehbar die Nutzungssituation ist.",
    "external_interruption_frequency": "Wie häufig Unterbrechungen von außen zu erwarten sind.",
    "attention_recovery_support": "Wie leicht man nach einer Ablenkung wieder in die Aufgabe zurückfindet.",
}


def selected_label_for_value(value: int) -> str:
    if value <= 24:
        return "Sehr niedrig"

    if value <= 49:
        return "Niedrig bis moderat"

    if value <= 74:
        return "Deutlich vorhanden"

    return "Stark ausgeprägt"


def build_detected_scenario_context(
    dimensions: dict,
) -> dict:
    task = dimensions.get("primary_task") or (
        dimensions.get("task_options", [{}])[0]
        if dimensions.get("task_options")
        else {}
    )

    environment = (
        dimensions.get("environment_options", [{}])[0]
        if dimensions.get("environment_options")
        else {}
    )

    environment_text = environment.get("label", "")

    if environment.get("description"):
        environment_text += f": {environment['description']}"

    return {
        "device": dimensions.get(
            "detected_device",
            "Laptop",
        ),
        "task": {
            "label": task.get("label", ""),
            "description": task.get(
                "description",
                "",
            ),
        },
        "environment": environment_text,
    }


def definition_for_signal(
    signal: dict,
    attribute: str | None = None,
    fallback: str = (
        "Automatisch erkannter Wert für dieses Szenario auf einer Skala von 0 bis 100."
    ),
) -> str:
    if attribute and attribute in ATTRIBUTE_DEFINITIONS:
        return ATTRIBUTE_DEFINITIONS[attribute]

    definition = str(signal.get("description") or "").strip()
    return definition or fallback


def _render_dimension_header(
    label: str,
    selected_value: int,
) -> None:
    selected_label = selected_label_for_value(selected_value)

    title_column, value_column, badge_column = st.columns(
        [1, 0.14, 0.36],
        gap="small",
    )

    with title_column:
        st.markdown(
            (
                '<div class="cogsim-dimension-header__title">'
                f"{escape(label)}"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

    with value_column:
        st.markdown(
            (
                '<div class="cogsim-dimension-header__value">'
                f"{selected_value}"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

    with badge_column:
        st.markdown(
            (
                '<div class="cogsim-dimension-header__badge">'
                f"{escape(selected_label)}"
                "</div>"
            ),
            unsafe_allow_html=True,
        )


def _render_dimension_scale(
    minimum_description: str,
    maximum_description: str,
) -> None:
    st.markdown(
        (
            '<div class="cogsim-dimension-scale">'
            '<span class="cogsim-dimension-scale__minimum">'
            f"{escape(minimum_description)}"
            "</span>"
            '<span class="cogsim-dimension-scale__maximum">'
            f"{escape(maximum_description)}"
            "</span>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _render_dimension_info(
    *,
    group_key: str,
    attribute: str,
    label: str,
    definition: str,
    signal: dict,
) -> None:
    with st.popover(
        "Erklärung",
        icon=":material/info:",
        use_container_width=False,
        key=f"dimension_info_{group_key}_{attribute}",
    ):
        minimum_description = str(
            signal.get("scale_min_description", "geringe Ausprägung")
        )
        maximum_description = str(
            signal.get("scale_max_description", "starke Ausprägung")
        )
        rationale = str(signal.get("rationale") or "").strip()

        st.markdown(f"**{label}**")
        st.write(definition)
        st.markdown(
            (
                f"- **Niedriger Wert:** {minimum_description}\n"
                f"- **Hoher Wert:** {maximum_description}"
            )
        )
        if rationale:
            st.markdown("**Warum wurde dieser Wert erkannt?**")
            st.write(rationale)


def _render_dimension_control(
    *,
    group_key: str,
    attribute: str,
    signal: dict,
) -> None:
    label = (
        MODEL_ATTRIBUTE_LABELS.get(attribute)
        or signal.get("name")
        or attribute.replace("_", " ").title()
    )

    current_value = int(signal.get("value", 50))
    slider_key = f"dimension_value_{group_key}_{attribute}"
    display_value = int(st.session_state.get(slider_key, current_value))

    with st.container(
        key=f"dimension_card_{group_key}_{attribute}",
    ):
        _render_dimension_header(
            label,
            display_value,
        )

        selected_value = st.slider(
            label,
            min_value=0,
            max_value=100,
            value=current_value,
            key=slider_key,
            help=signal.get("description") or None,
            label_visibility="collapsed",
        )

        signal["value"] = selected_value
        signal["label"] = selected_label_for_value(selected_value)

        _render_dimension_scale(
            str(
                signal.get(
                    "scale_min_description",
                    "0",
                )
            ),
            str(
                signal.get(
                    "scale_max_description",
                    "100",
                )
            ),
        )

        _render_dimension_info(
            group_key=group_key,
            attribute=attribute,
            label=label,
            definition=definition_for_signal(signal, attribute),
            signal=signal,
        )


def _render_signal_group(
    group_key: str,
    signals: dict,
) -> None:
    if not signals:
        st.caption("Für diesen Bereich wurden keine Werte erkannt.")
        return

    signal_items = list(signals.items())

    left_column, right_column = st.columns(
        2,
        gap="medium",
    )

    for index, (attribute, signal) in enumerate(signal_items):
        target_column = left_column if index % 2 == 0 else right_column

        with target_column:
            _render_dimension_control(
                group_key=group_key,
                attribute=attribute,
                signal=signal,
            )


def render_dimensions_section(
    dimensions: dict,
) -> dict:
    st.markdown(
        (
            '<div class="cogsim-dimensions-intro">'
            '<div class="cogsim-dimensions-intro__title">'
            "Erkannte Anforderungen prüfen"
            "</div>"
            '<div class="cogsim-dimensions-intro__text">'
            "Jede Karte beschreibt eine Eigenschaft, die die spätere Simulation "
            "beeinflusst. Die Skala reicht immer von 0 bis 100 und ist ein "
            "Einschätzungswert, keine Prozentangabe. 0 bedeutet sehr gering, "
            "100 sehr stark ausgeprägt. Konkrete Szenarioangaben, zum Beispiel "
            "die Anzahl wichtiger Arbeitsschritte, werden für die Modellierung "
            "ebenfalls auf diesen Wertebereich übertragen."
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    focused_area = st.session_state.get("dimension_focus_area")
    focused_group_key = (
        f"{focused_area}_signals"
        if focused_area in {"task", "interface", "environment"}
        else None
    )
    signal_groups = list(SIGNAL_GROUPS)
    if focused_group_key:
        signal_groups.sort(
            key=lambda item: 0 if item[0] == focused_group_key else 1
        )

    tabs = st.tabs([label for _, label in signal_groups])

    for tab, (group_key, _) in zip(
        tabs,
        signal_groups,
    ):
        signals = dimensions.get(
            group_key,
            {},
        )

        with tab:
            _render_signal_group(
                group_key,
                signals,
            )

    return dimensions
