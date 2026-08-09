from html import escape

import streamlit as st

from backend.domains.evaluation.registries.metrics import (
    build_default_evaluation_metrics_selection,
    get_predefined_evaluation_metrics,
)
from backend.domains.evaluation.schemas.evaluation_metrics import (
    EvaluationGoalSelection,
)
from backend.domains.evaluation.services.metric_selection import (
    resolve_evaluation_goal_selection,
)
from frontend.shared.ui.icons import render_icon

DEFAULT_METRIC_IDS: set[str] = set()
RETIRED_METRIC_IDS = {
    "dyslexia_reading_load",
    "adhd_interaction_load",
}


METRIC_ICON_BY_ID = {
    "cognitive_load": "brain",
    "error_risk": "shield-alert",
    "completion_efficiency": "gauge",
    "task_success_score": "check-circle-2",
    "completion_time": "timer",
    "time_limit_risk": "clock-alert",
}

METRIC_DISPLAY_CONTENT = {
    "cognitive_load": {
        "description": (
            "Zeigt, welche Schritte besonders viel Konzentration, Mitdenken "
            "oder Erinnern verlangen."
        ),
        "example": (
            "Gemessen wird zum Beispiel, ob ein Schritt viele Informationen, "
            "Entscheidungen und Merkanforderungen gleichzeitig enthält."
        ),
    },
    "error_risk": {
        "description": (
            "Zeigt, an welchen Stellen Eingaben, Auswahlentscheidungen oder "
            "Klicks leicht schiefgehen können."
        ),
        "example": (
            "Gemessen wird zum Beispiel, ob ein Schritt viele Pflichtfelder, "
            "ähnliche Optionen oder fehlerkritische Bestätigungen enthält."
        ),
    },
    "completion_efficiency": {
        "description": (
            "Zeigt, wie flüssig ein Profil durch die Aufgabe kommt und wo "
            "unnötiger Aufwand entsteht."
        ),
        "example": (
            "Gemessen wird zum Beispiel, ob ein Profil viele Umwege, "
            "Wiederholungen oder Verzögerungen im Ablauf hat."
        ),
    },
    "task_success_score": {
        "description": (
            "Zeigt, wie wahrscheinlich es im Modell ist, dass ein Profil die "
            "Aufgabe verständlich und ohne größere Hürden abschließen kann."
        ),
        "example": (
            "Gemessen wird zum Beispiel, ob Belastung, Fehlerrisiko und "
            "Orientierung insgesamt noch einen erfolgreichen Abschluss erwarten lassen."
        ),
    },
    "completion_time": {
        "description": (
            "Zeigt, wie lange ein Profil für die Aufgabe voraussichtlich braucht."
        ),
        "example": (
            "Gemessen wird die simulierte Zeit vom ersten bis zum letzten "
            "Arbeitsschritt, inklusive Verzögerungen."
        ),
    },
    "time_limit_risk": {
        "description": (
            "Zeigt, ob die Aufgabe unter Zeitdruck knapp werden kann."
        ),
        "example": (
            "Gemessen wird, ob die simulierte Bearbeitungszeit im Verhältnis "
            "zu einem angenommenen Zeitlimit kritisch wird."
        ),
    },
}


def build_metrics_selection(
    metric_ids: list[str],
) -> dict:
    metric_ids = [
        metric_id
        for metric_id in metric_ids
        if metric_id not in RETIRED_METRIC_IDS
    ]
    if not metric_ids:
        return {
            "selected_metrics": [],
            "custom_metric_requests": [],
        }

    selection = build_default_evaluation_metrics_selection(metric_ids)
    selection.custom_metric_requests = []

    return selection.model_dump()


def build_evaluation_goal_selection(
    goal_ids: list[str],
) -> dict:
    return EvaluationGoalSelection(
        selected_goal_ids=goal_ids,
        custom_metric_requests=[],
    ).model_dump()


def build_evaluation_selection_bundle(
    goal_ids: list[str],
) -> dict:
    goal_selection = EvaluationGoalSelection(
        selected_goal_ids=goal_ids,
        custom_metric_requests=[],
    )

    resolved = resolve_evaluation_goal_selection(goal_selection)

    return {
        "evaluation_goal_selection": (goal_selection.model_dump()),
        "evaluation_metrics": (resolved.selected_metrics.model_dump()),
        "resolved_evaluation_selection": (resolved.model_dump()),
    }


def build_metric_selection_bundle(
    metric_ids: list[str],
) -> dict:
    if not metric_ids:
        return {
            "evaluation_goal_selection": None,
            "evaluation_metrics": None,
            "resolved_evaluation_selection": None,
        }

    return {
        "evaluation_goal_selection": None,
        "evaluation_metrics": build_metrics_selection(metric_ids),
        "resolved_evaluation_selection": None,
    }


def _metric_display_content(metric) -> dict:
    display = METRIC_DISPLAY_CONTENT.get(metric.metric_id, {})

    return {
        "title": metric.name,
        "description": display.get("description") or metric.description,
        "example": display.get("example"),
        "icon": METRIC_ICON_BY_ID.get(metric.metric_id, "bar-chart-3"),
    }


def _render_metric_card(metric) -> bool:
    content = _metric_display_content(metric)
    example = ""
    if content.get("example"):
        example = (
            '<div class="cogsim-evaluation-card-example">'
            "<span>Beispiel</span>"
            f"{escape(content['example'])}"
            "</div>"
        )

    with st.container(
        key=f"evaluation_metric_card_{metric.metric_id}",
    ):
        selection_key = f"evaluation_metric_{metric.metric_id}"

        if selection_key not in st.session_state:
            st.session_state[selection_key] = False

        st.markdown(
            (
                '<div class="cogsim-evaluation-card-header">'
                '<div class="cogsim-evaluation-card-icon">'
                f"{render_icon(content['icon'], size=19, stroke_width=1.8)}"
                "</div>"
                '<div class="cogsim-evaluation-card-copy">'
                '<div class="cogsim-evaluation-card-title">'
                f"{escape(content['title'])}"
                "</div>"
                '<div class="cogsim-evaluation-card-description">'
                f"{escape(content['description'])}"
                "</div>"
                f"{example}"
                "</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        selected = st.checkbox(
            "Auswählen",
            key=selection_key,
        )

    return selected


def render_metrics_section(
    _dimensions: dict,
) -> dict:
    st.markdown(
        (
            '<div class="cogsim-evaluation-intro">'
            '<div class="cogsim-evaluation-intro__title">'
            "Was möchtest du später in den Ergebnissen sehen?"
            "</div>"
            '<div class="cogsim-evaluation-intro__text">'
            "Wähle die Kennwerte aus, die CogSim für die ausgewählten "
            "Nutzerprofile vergleichen soll. Du kannst dich auf wenige Werte "
            "konzentrieren, wenn dich nur bestimmte Fragen interessieren."
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    selected_metric_ids: list[str] = []
    metrics = [
        metric
        for metric in get_predefined_evaluation_metrics()
        if metric.metric_id not in RETIRED_METRIC_IDS
    ]

    left_column, right_column = st.columns(
        2,
        gap="large",
    )

    for index, metric in enumerate(metrics):
        target_column = left_column if index % 2 == 0 else right_column

        with target_column:
            if _render_metric_card(metric):
                selected_metric_ids.append(metric.metric_id)

    return build_metric_selection_bundle(
        selected_metric_ids,
    )
