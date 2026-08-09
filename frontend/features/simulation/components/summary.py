from html import escape

import streamlit as st

from frontend.features.simulation.formatting import (
    metric_value as _metric_value,
    number as _number,
    value_from_mapping as _value_from_mapping,
)
from frontend.features.simulation.utils.helpers import profile_color
from frontend.shared.ui.icons import render_icon


def metric_is_selected(
    selected_metric_ids: set[str] | None,
    metric_id: str,
) -> bool:
    return selected_metric_ids is None or metric_id in selected_metric_ids


def _event_count(profile: dict) -> int:
    events = profile.get("events", [])
    if events:
        return len(events)
    return sum(len(item.get("events", [])) for item in profile.get("timeline", []))


def _format_seconds(value: float) -> str:
    seconds = max(0, int(round(value)))
    minutes, remaining_seconds = divmod(seconds, 60)
    if minutes:
        return f"{minutes}:{remaining_seconds:02d} min"
    return f"{remaining_seconds} s"


def _task_success_interpretation(value: float) -> str:
    if value >= 75:
        return "hoher Aufgabenerfolgswert"
    if value >= 50:
        return "mittlerer Aufgabenerfolgswert"
    return "niedriger Aufgabenerfolgswert"


def _safe_summary_text(value: object) -> str:
    text = str(value or "").strip()
    normalized = text.strip("*").strip().lower()
    if normalized in {
        "<div>",
        "</div>",
        "<section>",
        "</section>",
        "<article>",
        "</article>",
    }:
        return ""
    return escape(text)


def _status_icon(severity: str) -> str:
    icon_name = {
        "success": "check-circle-2",
        "notice": "check-circle-2",
        "warning": "shield-alert",
        "danger": "shield-alert",
        "critical": "shield-alert",
    }.get(severity, "check-circle-2")
    return render_icon(icon_name, size=25, stroke_width=2.15)


def _build_fallback_summary(profiles: list[dict]) -> dict:
    slowest_profile = max(
        profiles,
        key=lambda profile: float(profile.get("completion_time_seconds") or 0),
    )
    completion_seconds = float(slowest_profile.get("completion_time_seconds") or 0)
    goms_seconds = sum(
        float(step.get("planned_duration_seconds") or 0)
        for step in (slowest_profile.get("task_step_durations") or [])
    )
    if not goms_seconds:
        goms_seconds = sum(
            float(item.get("base_step_duration") or 0)
            for item in (slowest_profile.get("timeline") or [])
            if item.get("step_status") == "completed"
        )
    deviation = completion_seconds - goms_seconds
    deviation_percent = (deviation / goms_seconds * 100) if goms_seconds else 0
    total_events = sum(_event_count(profile) for profile in profiles)
    has_aborted_profile = any(profile.get("completed") is False for profile in profiles)
    min_success_profile = min(
        profiles,
        key=lambda profile: _metric_value(profile, "task_success_score"),
    )
    min_success = _metric_value(min_success_profile, "task_success_score")
    profile_names = ", ".join(
        str(profile.get("profile_label") or profile.get("profile_id") or "Profil")
        for profile in profiles
    )

    if has_aborted_profile:
        status = {
            "severity": "critical",
            "label": "Mindestens ein Profil hat abgebrochen",
            "explanation": (
                "Die Simulation konnte nicht für alle Profile vollständig "
                "abgeschlossen werden."
            ),
            "details": "",
        }
    elif total_events:
        status = {
            "severity": "warning",
            "label": "Simulation abgeschlossen mit Auffälligkeiten",
            "explanation": (
                "Die Aufgabe wurde abgeschlossen, dabei wurden aber kritische "
                "Situationen im Verlauf erkannt."
            ),
            "details": "",
        }
    else:
        status = {
            "severity": "success",
            "label": "Simulation erfolgreich abgeschlossen",
            "explanation": (
                "Alle ausgewählten Profile konnten die simulierte Aufgabe "
                "abschließen."
            ),
            "details": "",
        }

    return {
        "status": status,
        "primary_completion_time": {
            "label": "Simulierte Bearbeitungszeit",
            "value_label": _format_seconds(completion_seconds),
            "basis_label": (
                "längste simulierte Bearbeitungszeit "
                f"({slowest_profile.get('profile_label', 'Profil')})"
            ),
            "goms_basis_label": _format_seconds(goms_seconds),
            "deviation_label": (
                f"{deviation:+.0f} Sek. beziehungsweise {deviation_percent:+.0f} %"
            ),
            "explanation": (
                "Die Basiszeit beschreibt die geplante Bearbeitungsdauer. "
                "Die Simulation ergänzt profilspezifische Belastungen, Events "
                "und mögliche Wiederholungen."
            ),
        },
        "secondary_items": [
            {
                "label": f"{len(profiles)} Nutzerprofile verglichen",
                "value": str(len(profiles)),
                "interpretation": profile_names,
                "explanation": (
                    "Das Szenario wurde mit den ausgewählten Profilen simuliert, "
                    "damit Unterschiede sichtbar werden."
                ),
            },
            {
                "label": "Erfolgreiche Aufgabenbearbeitung",
                "value": f"{min_success:.0f} von 100",
                "interpretation": (
                    f"{_task_success_interpretation(min_success)} "
                    f"bei {min_success_profile.get('profile_label', 'Profil')}"
                ),
                "explanation": (
                    "Der Wert beschreibt, wie gut die Aufgabe im Modell "
                    "voraussichtlich abgeschlossen werden kann."
                ),
            },
            {
                "label": f"{total_events} auffällige Ereignisse erkannt",
                "value": str(total_events),
                "interpretation": (
                    "keine auffälligen Ereignisse"
                    if total_events == 0
                    else "auffällige Situationen im Aufgabenverlauf"
                ),
                "explanation": (
                    "Events markieren besondere Situationen, etwa hohe "
                    "Belastung, sinkende Aufmerksamkeit oder Wiederholungen."
                ),
            },
        ],
        "explanation": (
            "Die Zusammenfassung basiert auf den berechneten Profil-Ergebnissen."
        ),
    }


def render_overview_kpi_cards(
    profiles: list[dict],
    selected_metric_ids: set[str] | None = None,
    presentation: dict | None = None,
) -> None:
    summary = (presentation or {}).get("summary", {})
    if not profiles:
        return
    if not summary:
        summary = _build_fallback_summary(profiles)
    status = summary.get("status", {})
    completion_time = summary.get("primary_completion_time", {})
    secondary_items = summary.get("secondary_items", [])
    severity = status.get("severity", "success")
    status_details = _safe_summary_text(status.get("details", ""))
    status_details_markup = (
        f"<small>{status_details}</small>"
        if status_details
        else ""
    )
    secondary_markup = "\n".join(
        (
            '<article class="cogsim-result-summary-small-card">'
            f'<span>{_safe_summary_text(item.get("label", ""))}</span>'
            f'<strong>{_safe_summary_text(item.get("value", ""))}</strong>'
            f'<small>{_safe_summary_text(item.get("interpretation", ""))}</small>'
            f'<p>{_safe_summary_text(item.get("explanation", ""))}</p>'
            "</article>"
        )
        for item in secondary_items[:3]
    )
    st.markdown(
        f"""
        <section class="cogsim-result-summary-panel cogsim-result-summary-panel--{_safe_summary_text(severity)}">
            <div class="cogsim-result-summary-header">
                <span>Kurze Zusammenfassung</span>
                <small>{_safe_summary_text(summary.get("explanation", ""))}</small>
            </div>
            <div class="cogsim-result-summary-primary-grid">
                <article class="cogsim-result-status-card cogsim-result-status-card--{_safe_summary_text(severity)}">
                    <div class="cogsim-result-status-card__icon">{_status_icon(str(severity))}</div>
                    <div>
                        <span>Gesamtstatus</span>
                        <h4>{_safe_summary_text(status.get("label", ""))}</h4>
                        <p>{_safe_summary_text(status.get("explanation", ""))}</p>
                        {status_details_markup}
                    </div>
                </article>
                <article class="cogsim-result-time-card">
                    <span>{_safe_summary_text(completion_time.get("label", ""))}</span>
                    <strong>{_safe_summary_text(completion_time.get("value_label", ""))}</strong>
                    <small>{_safe_summary_text(completion_time.get("basis_label", ""))}</small>
                    <div class="cogsim-result-time-card__basis">
                        <div>
                            <span>Basiszeit</span>
                            <b>{_safe_summary_text(completion_time.get("goms_basis_label", ""))}</b>
                        </div>
                        <div>
                            <span>Abweichung</span>
                            <b>{_safe_summary_text(completion_time.get("deviation_label", ""))}</b>
                        </div>
                    </div>
                    <p>{_safe_summary_text(completion_time.get("explanation", ""))}</p>
                </article>
            </div>
            <div class="cogsim-result-summary-small-grid">
                {secondary_markup}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_result_section_heading(
    presentation: dict,
    section_id: str,
) -> None:
    section = (presentation.get("sections") or {}).get(section_id)
    if not section:
        return
    st.markdown(
        (
            '<div class="cogsim-result-section-copy">'
            f'<h4>{escape(section.get("title", ""))}</h4>'
            f'<p>{escape(section.get("short_explanation", ""))}</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def _profile_metric_bar(
    *,
    profile: dict,
    value: float,
    index: int,
    suffix: str = "",
    max_value: float = 100,
) -> str:
    color = profile_color(profile, index)
    width = max(
        0,
        min(
            100,
            (float(value) / max_value * 100) if max_value else float(value),
        ),
    )
    return (
        '<div class="cogsim-profile-score-row">'
        '<span class="cogsim-profile-score-row__label">'
        f'{escape(str(profile["profile_label"]))}'
        "</span>"
        '<div class="cogsim-profile-score-row__track">'
        '<span class="cogsim-profile-score-row__bar" '
        f'style="width:{width:.1f}%;background:{color};"></span>'
        "</div>"
        '<span class="cogsim-profile-score-row__value">'
        f"{escape(str(_number(value)))}{escape(suffix)}"
        "</span>"
        "</div>"
    )


def render_profile_comparison_report(
    profiles: list[dict],
    selected_metric_ids: set[str] | None,
) -> None:
    metrics = [
        {
            "id": "cognitive_load",
            "title": "Kognitive Belastung",
            "subtitle": "Wo entsteht besonders viel mentaler Aufwand?",
            "suffix": "",
            "value": lambda profile: _metric_value(profile, "cognitive_load"),
        },
        {
            "id": "error_risk",
            "title": "Fehlerrisiko",
            "subtitle": "Bei welchem Profil wirken Schritte unsicherer?",
            "suffix": "",
            "value": lambda profile: _metric_value(profile, "error_risk"),
        },
        {
            "id": "task_success_score",
            "title": "Aufgabenerfolg",
            "subtitle": "Wie gut kann die Aufgabe voraussichtlich gelingen?",
            "suffix": "%",
            "value": lambda profile: _metric_value(profile, "task_success_score"),
        },
        {
            "id": "completion_time",
            "title": "Bearbeitungszeit",
            "subtitle": "Welches Profil benötigt am längsten?",
            "suffix": " s",
            "max_value": max(
                [
                    float(profile.get("completion_time_seconds") or 0)
                    for profile in profiles
                ]
                + [1]
            ),
            "value": lambda profile: float(
                profile.get("completion_time_seconds") or 0
            ),
        },
    ]
    visible_metrics = [
        metric
        for metric in metrics
        if metric_is_selected(selected_metric_ids, metric["id"])
    ]
    if not visible_metrics:
        return

    cards = []
    for metric in visible_metrics:
        rows = "".join(
            _profile_metric_bar(
                profile=profile,
                value=metric["value"](profile),
                index=index,
                suffix=metric.get("suffix", ""),
                max_value=metric.get("max_value", 100),
            )
            for index, profile in enumerate(profiles)
        )
        cards.append(
            (
                '<article class="cogsim-profile-comparison-card">'
                '<div class="cogsim-profile-comparison-card__title">'
                f'{escape(metric["title"])}'
                "</div>"
                '<div class="cogsim-profile-comparison-card__subtitle">'
                f'{escape(metric["subtitle"])}'
                "</div>"
                '<div class="cogsim-profile-comparison-card__rows">'
                f"{rows}"
                "</div>"
                "</article>"
            )
        )

    st.markdown(
        (
            '<section class="cogsim-profile-comparison-panel">'
            '<div class="cogsim-result-section-heading">'
            '<span>Profilvergleich</span>'
            '<small>Direkter Vergleich der ausgewählten Nutzerprofile</small>'
            "</div>"
            '<div class="cogsim-profile-comparison-grid">'
            f"{''.join(cards)}"
            "</div>"
            "</section>"
        ),
        unsafe_allow_html=True,
    )


def render_profile_detail_kpi_cards(profile: dict) -> None:
    metrics = profile.get("metrics", {})
    state = profile.get("final_state", {})
    cards = [
        {
            "label": "Kognitive Belastung",
            "value": _number(_metric_value(profile, "cognitive_load")),
            "detail": "finaler Simulationswert",
            "score": _metric_value(profile, "cognitive_load"),
            "tone": "warning",
        },
        {
            "label": "Fehlerrisiko",
            "value": _number(_metric_value(profile, "error_risk")),
            "detail": "höher bedeutet kritischer",
            "score": _metric_value(profile, "error_risk"),
            "tone": "danger",
        },
        {
            "label": "Aufgabenerfolg",
            "value": _number(_value_from_mapping(metrics, "task_success_score", 0)),
            "detail": "voraussichtlicher Erfolg",
            "score": _value_from_mapping(metrics, "task_success_score", 0),
            "tone": "success",
        },
        {
            "label": "Bearbeitungszeit",
            "value": f"{_number(profile.get('completion_time_seconds') or 0)} s",
            "detail": "simulierte Gesamtdauer",
            "score": 68,
            "tone": "primary",
        },
        {
            "label": "Events",
            "value": len(profile.get("events", [])),
            "detail": "kritische Hinweise",
            "score": min(100, len(profile.get("events", [])) * 18),
            "tone": "danger" if profile.get("events") else "success",
        },
        {
            "label": "Aufmerksamkeit",
            "value": _number(state.get("attention", 0)),
            "detail": "am Ende des Laufs",
            "score": state.get("attention", 0),
            "tone": "primary",
        },
    ]
    markup = "".join(
        (
            '<article class="cogsim-profile-kpi-card '
            f'cogsim-profile-kpi-card--{escape(card["tone"])}">'
            '<div class="cogsim-profile-kpi-card__label">'
            f'{escape(str(card["label"]))}'
            "</div>"
            '<div class="cogsim-profile-kpi-card__value">'
            f'{escape(str(card["value"]))}'
            "</div>"
            '<div class="cogsim-profile-kpi-card__detail">'
            f'{escape(str(card["detail"]))}'
            "</div>"
            '<div class="cogsim-profile-kpi-card__spark" '
            f'style="--score:{float(card["score"]) * 3.6:.1f}deg;"></div>'
            "</article>"
        )
        for card in cards
    )
    st.markdown(
        '<div class="cogsim-profile-kpi-grid">' + markup + "</div>",
        unsafe_allow_html=True,
    )
