from html import escape

import streamlit as st

from frontend.features.models.common import (
    model_attribute_value,
)
from frontend.features.simulation.utils.helpers import profile_color

USER_ATTRIBUTES = (
    (
        "reading_difficulty",
        "Leseschwierigkeit",
    ),
    (
        "sublexical_decoding_stability",
        "Dekodierstabilität",
    ),
    (
        "orthographic_processing_stability",
        "Orthografische Verarbeitungsstabilität",
    ),
    (
        "parallel_letter_processing_stability",
        "Parallele Buchstabenverarbeitung",
    ),
    (
        "attention_stability",
        "Aufmerksamkeitsstabilität",
    ),
    (
        "working_memory_stability",
        "Arbeitsgedächtnisstabilität",
    ),
    (
        "distraction_sensitivity",
        "Ablenkungsempfindlichkeit",
    ),
    (
        "task_switching_difficulty",
        "Schwierigkeit beim Aufgabenwechsel",
    ),
    (
        "vigilance_stability",
        "Daueraufmerksamkeitsstabilität",
    ),
    (
        "inhibitory_control",
        "Inhibitionskontrolle",
    ),
    (
        "attention_switching_stability",
        "Aufmerksamkeitswechsel-Stabilität",
    ),
    (
        "divided_attention_capacity",
        "Kapazität geteilter Aufmerksamkeit",
    ),
    (
        "omission_tendency",
        "Auslassungstendenz",
    ),
    (
        "reaction_variability",
        "Reaktionsschwankung",
    ),
)


USER_ATTRIBUTE_DESCRIPTIONS = {
    "reading_difficulty": "Beschreibt, wie stark Lesen für das Profil erschwert ist.",
    "sublexical_decoding_stability": "Beschreibt, wie stabil einzelne Buchstaben und Wortbestandteile erkannt werden.",
    "orthographic_processing_stability": "Beschreibt, wie stabil Schreibweisen und Wortmuster verarbeitet werden.",
    "parallel_letter_processing_stability": "Beschreibt, wie gut mehrere Buchstaben gleichzeitig erfasst werden.",
    "attention_stability": "Beschreibt, wie gut Aufmerksamkeit über die Aufgabe gehalten wird.",
    "working_memory_stability": "Beschreibt, wie stabil Informationen kurzzeitig im Kopf behalten werden.",
    "distraction_sensitivity": "Beschreibt, wie stark äußere Reize die Bearbeitung stören können.",
    "task_switching_difficulty": "Beschreibt, wie anspruchsvoll Wechsel zwischen Teilaufgaben sind.",
    "vigilance_stability": "Beschreibt, wie stabil Daueraufmerksamkeit bei längeren Aufgaben bleibt.",
    "inhibitory_control": "Beschreibt, wie gut irrelevante Impulse oder Ablenkungen unterdrückt werden.",
    "attention_switching_stability": "Beschreibt, wie stabil Aufmerksamkeit gezielt umgelenkt werden kann.",
    "divided_attention_capacity": "Beschreibt, wie gut mehrere Informationsquellen parallel beachtet werden.",
    "omission_tendency": "Beschreibt, wie wahrscheinlich Inhalte oder Schritte übersehen werden.",
    "reaction_variability": "Beschreibt, wie stark die Reaktionsgeschwindigkeit schwankt.",
}


USER_MODEL_READONLY_NOTICE = (
    "Die Profilwerte sind feste, reproduzierbare Referenzannahmen und können "
    "an dieser Stelle nicht verändert werden."
)


def build_user_model_views(
    user_model: dict,
    user_models: dict[str, dict] | None = None,
) -> list[dict]:
    if user_models:
        return [
            {
                "profile_id": profile_id,
                "profile_label": model.get(
                    "user_type",
                    profile_id,
                ),
                "user_model": model,
            }
            for profile_id, model in user_models.items()
        ]

    if user_model:
        return [
            {
                "profile_id": user_model.get(
                    "profile_id",
                    "generic",
                ),
                "profile_label": user_model.get(
                    "user_type",
                    "Generisch",
                ),
                "user_model": user_model,
            }
        ]

    return []


def build_user_model_comparison_rows(
    user_model: dict,
    user_models: dict[str, dict] | None = None,
) -> list[dict]:
    profiles = build_user_model_views(
        user_model,
        user_models,
    )

    rows = []

    for attribute_id, label in USER_ATTRIBUTES:
        row = {
            "Attribut-ID": attribute_id,
            "Attribut": label,
            "Beschreibung": USER_ATTRIBUTE_DESCRIPTIONS.get(attribute_id, ""),
        }

        for profile in profiles:
            row[profile["profile_label"]] = model_attribute_value(
                profile["user_model"].get(attribute_id)
            )

        rows.append(row)

    return rows


def _render_user_model_comparison_cards(
    rows: list[dict],
) -> None:
    cards = []
    for row in rows:
        attribute_label = escape(str(row.get("Attribut", "")))
        attribute_description = escape(str(row.get("Beschreibung", "")))
        profile_values = []
        profile_index = 0
        for profile_label, value in row.items():
            if profile_label in {"Attribut", "Attribut-ID", "Beschreibung"}:
                continue
            try:
                numeric_value = max(0.0, min(100.0, float(value)))
            except (TypeError, ValueError):
                numeric_value = 0.0
            color = profile_color(
                {
                    "profile_id": str(profile_label).lower(),
                    "profile_label": str(profile_label),
                },
                profile_index,
            )
            profile_index += 1

            profile_values.append(
                (
                    '<div class="cogsim-user-comparison-value-row">'
                    '<div class="cogsim-user-comparison-value-row__label">'
                    f"<span>{escape(str(profile_label))}</span>"
                    f"<strong>{escape(str(value))}</strong>"
                    "</div>"
                    '<div class="cogsim-user-comparison-value-row__track">'
                    '<span style="'
                    f"width:{numeric_value:.0f}%; background:{escape(color)};"
                    '"></span>'
                    "</div>"
                    "</div>"
                )
            )

        cards.append(
            (
                '<div class="cogsim-user-comparison-card">'
                '<div class="cogsim-user-comparison-card__attribute">'
                f"{attribute_label}"
                "</div>"
                '<p class="cogsim-user-comparison-card__description">'
                f"{attribute_description}"
                "</p>"
                '<div class="cogsim-user-comparison-card__values">'
                f"{''.join(profile_values)}"
                "</div>"
                "</div>"
            )
        )

    st.markdown(
        '<div class="cogsim-user-comparison-grid">'
        + "".join(cards)
        + "</div>",
        unsafe_allow_html=True,
    )


def render_user_model_review(
    user_model: dict,
    user_models: dict[str, dict] | None = None,
) -> dict:
    profile_views = build_user_model_views(
        user_model,
        user_models,
    )

    if not profile_views:
        st.warning("Keine Nutzerprofile vorhanden.")
        return {}

    st.markdown(
        (
            '<div class="cogsim-model-section-header">'
            '<div class="cogsim-model-section-title">'
            "Vergleich der Nutzerprofile"
            "</div>"
            '<div class="cogsim-model-section-description">'
            f"{USER_MODEL_READONLY_NOTICE}"
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    with st.container(
        key="user_model_comparison",
    ):
        comparison_rows = build_user_model_comparison_rows(
            user_model,
            user_models,
        )
        _render_user_model_comparison_cards(comparison_rows)

    return {}
