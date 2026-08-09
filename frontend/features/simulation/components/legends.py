from html import escape

import streamlit as st

from frontend.shared.ui.icons import render_icon


def _format_seconds(value: float) -> str:
    seconds = max(0, int(round(value)))
    minutes, remaining_seconds = divmod(seconds, 60)
    if minutes:
        return f"{minutes} Min. {remaining_seconds} Sek."
    return f"{remaining_seconds} Sek."


def _duration_bar_markup(profiles: list[dict]) -> str:
    if not profiles:
        return ""
    max_duration = max(
        [float(profile.get("completion_time_seconds") or 0) for profile in profiles]
        or [1]
    ) or 1
    rows = []
    for profile in profiles:
        label = str(profile.get("profile_label") or "Profil")
        duration = float(profile.get("completion_time_seconds") or 0)
        width = max(8, min(100, duration / max_duration * 100))
        rows.append(
            (
                '<div class="cogsim-context-time-row">'
                f'<span>{escape(label)}</span>'
                '<div class="cogsim-context-time-row__track">'
                f'<i style="width:{width:.0f}%"></i>'
                "</div>"
                f'<small>{escape(_format_seconds(duration))}</small>'
                "</div>"
            )
        )
    return "".join(rows)


def _goms_basis_time(profiles: list[dict]) -> float:
    for profile in profiles:
        durations = profile.get("task_step_durations") or []
        basis = sum(float(step.get("planned_duration_seconds") or 0) for step in durations)
        if basis:
            return basis
        timeline = profile.get("timeline") or []
        basis = sum(
            float(item.get("base_step_duration") or 0)
            for item in timeline
            if item.get("step_status") == "completed"
        )
        if basis:
            return basis
    return 0.0


def render_overview_result_context(
    profiles: list[dict],
    presentation: dict,
    selected_metric_ids: set[str] | None,
) -> None:
    selected_metric_ids = selected_metric_ids or set()
    metric_items = [
        item
        for item in presentation.get("metric_legend", [])
        if not selected_metric_ids
        or item.get("metric_id") in selected_metric_ids
        or item.get("id") in selected_metric_ids
    ]
    event_items = presentation.get("event_legend", [])
    metric_labels = [
        str(item.get("label") or item.get("name") or "").strip()
        for item in metric_items
        if item.get("label") or item.get("name")
    ]
    event_labels = [
        str(item.get("label") or item.get("name") or "").strip()
        for item in event_items
        if item.get("label") or item.get("name")
    ]
    basis_time = _goms_basis_time(profiles)
    metric_chips = "".join(
        f"<span>{escape(label)}</span>"
        for label in (
            metric_labels[:4]
            or [
                "Bearbeitungseffizienz",
                "Aufgabenerfolg",
                "Fehlerrisiko",
                "Zeitlimit-Risiko",
            ]
        )
    )
    event_list = "".join(
        f"<li>{escape(label)}</li>" for label in event_labels[:4]
    ) or "<li>Keine Eventtypen vorhanden</li>"
    st.markdown(
        (
            '<section class="cogsim-overview-context-panel">'
            '<div class="cogsim-overview-context-panel__header">'
            "<span>So liest du die Ergebnisse</span>"
            "<p>CogSim simuliert denselben Aufgabenablauf mit unterschiedlichen "
            "Nutzerprofilen. Die Werte sind Modellwerte, keine gemessenen Nutzungsdaten.</p>"
            "</div>"
            '<div class="cogsim-overview-context-grid">'
            '<article class="cogsim-overview-context-card cogsim-overview-context-card--metrics">'
            f'<div class="cogsim-overview-context-card__icon">{render_icon("bar-chart-3", size=24, stroke_width=1.9)}</div>'
            "<strong>Metriken</strong>"
            "<p>Metriken fassen zentrale Ergebnisse der Simulation als Kennzahlen zusammen.</p>"
            f'<div class="cogsim-overview-context-card__chips">{metric_chips}</div>'
            "</article>"
            '<article class="cogsim-overview-context-card cogsim-overview-context-card--events">'
            f'<div class="cogsim-overview-context-card__icon">{render_icon("activity", size=24, stroke_width=1.9)}</div>'
            "<strong>Events</strong>"
            "<p>Events markieren Aufgabenschritte, an denen ein Schwellenwert erreicht wurde.</p>"
            f'<ul class="cogsim-overview-context-card__event-list">{event_list}</ul>'
            "</article>"
            '<article class="cogsim-overview-context-card cogsim-overview-context-card--time">'
            f'<div class="cogsim-overview-context-card__icon">{render_icon("timer", size=24, stroke_width=1.9)}</div>'
            "<strong>Bearbeitungszeit</strong>"
            "<p>Die Basiszeit ist der geplante Arbeitsumfang. Profilzeiten zeigen simulierte Abweichungen.</p>"
            '<div class="cogsim-context-time-bars">'
            f'<div class="cogsim-context-time-row cogsim-context-time-row--basis"><span>Basiszeit</span><small>{escape(_format_seconds(basis_time))}</small></div>'
            f'{_duration_bar_markup(profiles)}'
            "</div>"
            "</article>"
            '<article class="cogsim-overview-context-card cogsim-overview-context-card--scale">'
            f'<div class="cogsim-overview-context-card__icon">{render_icon("gauge", size=24, stroke_width=1.9)}</div>'
            "<strong>Skala 0–100</strong>"
            '<div class="cogsim-context-scale">'
            '<div class="cogsim-context-scale__track"><span></span></div>'
            '<div class="cogsim-context-scale__labels"><small>0 gering</small><small>50 mittel</small><small>100 hoch</small></div>'
            "</div>"
            '<div class="cogsim-context-scale__examples">'
            "<span>Hohe Aufmerksamkeit = günstig</span>"
            "<span>Hohes Fehlerrisiko = kritisch</span>"
            "</div>"
            "</article>"
            "</div>"
            "</section>"
        ),
        unsafe_allow_html=True,
    )


def _list_markup(items: list[str]) -> str:
    if not items:
        return ""
    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def render_result_legend_teasers(presentation: dict) -> None:
    metric_count = len(presentation.get("metric_legend", []))
    event_count = len(presentation.get("event_legend", []))
    st.markdown(
        (
            '<div class="cogsim-result-help-teaser-grid">'
            '<article class="cogsim-result-help-teaser">'
            "<span>Metriken</span>"
            f"<strong>{metric_count} Kennzahlen</strong>"
            "<p>Was bedeuten die Werte, welche Richtung ist günstig und welche "
            "Events hängen damit zusammen?</p>"
            "</article>"
            '<article class="cogsim-result-help-teaser">'
            "<span>Events</span>"
            f"<strong>{event_count} Eventtypen</strong>"
            "<p>Wann werden auffällige Situationen markiert und was bedeuten sie für die "
            "Interpretation der Simulation?</p>"
            "</article>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_metric_legend(presentation: dict) -> None:
    items = presentation.get("metric_legend", [])
    if not items:
        return
    with st.expander("Metriken verstehen", expanded=False):
        cards = []
        for item in items:
            cards.append(
                (
                    '<article class="cogsim-result-legend-card">'
                    f'<h5>{escape(item.get("label", ""))}</h5>'
                    f'<p>{escape(item.get("description", ""))}</p>'
                    '<div class="cogsim-result-legend-card__meta">'
                    f'<span>Wertebereich: {escape(item.get("value_range", ""))}</span>'
                    f'<span>Einheit: {escape(item.get("unit", ""))}</span>'
                    f'<span>Richtung: {escape(item.get("preferred_direction", ""))}</span>'
                    "</div>"
                    '<div class="cogsim-result-legend-card__section">'
                    "<strong>Wird beeinflusst durch</strong>"
                    f'{_list_markup(item.get("influencing_factors", []))}'
                    "</div>"
                    '<div class="cogsim-result-legend-card__section">'
                    "<strong>Zugehörige Events</strong>"
                    f'{_list_markup(item.get("related_events", []))}'
                    "</div>"
                    '<div class="cogsim-result-legend-card__section">'
                    "<strong>Für Designentscheidungen relevant bei</strong>"
                    f'{_list_markup(item.get("design_context", []))}'
                    "</div>"
                    "</article>"
                )
            )
        st.markdown(
            '<div class="cogsim-result-legend-grid">'
            + "".join(cards)
            + "</div>",
            unsafe_allow_html=True,
        )


def render_event_legend(presentation: dict) -> None:
    items = presentation.get("event_legend", [])
    if not items:
        return
    with st.expander("Events verstehen", expanded=False):
        cards = []
        for item in items:
            cards.append(
                (
                    '<article class="cogsim-result-legend-card">'
                    f'<h5>{escape(item.get("label", ""))}</h5>'
                    f'<p>{escape(item.get("description", ""))}</p>'
                    '<div class="cogsim-result-legend-card__meta">'
                    f'<span>Ausgelöst bei: {escape(item.get("trigger_description", ""))}</span>'
                    f'<span>Schwellenwert: {escape(str(item.get("trigger_value", "")))}</span>'
                    "</div>"
                    '<div class="cogsim-result-legend-card__section">'
                    "<strong>Mögliche Auswirkung</strong>"
                    f'{_list_markup(item.get("possible_consequences", []))}'
                    "</div>"
                    '<div class="cogsim-result-legend-card__section">'
                    "<strong>Beeinflusste Metriken</strong>"
                    f'{_list_markup(item.get("related_metrics", []))}'
                    "</div>"
                    '<div class="cogsim-result-legend-card__section">'
                    "<strong>Was sollte geprüft werden?</strong>"
                    f'{_list_markup(item.get("design_context", []))}'
                    "</div>"
                    "</article>"
                )
            )
        st.markdown(
            '<div class="cogsim-result-legend-grid">'
            + "".join(cards)
            + "</div>",
            unsafe_allow_html=True,
        )
