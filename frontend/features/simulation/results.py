import csv
import io
import json
import math
import re
from html import escape

import altair as alt
import streamlit as st
import streamlit.components.v1 as components

from frontend.features.simulation.formatting import task_step_display_label
from frontend.features.simulation.components.data import (
    build_additional_timeline_rows,
    build_available_timeline_metric_options,
    build_compact_timeline_rows,
    build_display_profile_views,
    build_metric_chart_rows,
    build_overview_duration_chart_rows,
    build_overview_metric_chart_rows,
    build_overview_metric_timeline_rows,
    build_profile_comparison_rows,
    build_profile_result_views,
    build_profile_metric_timeline_rows,
    build_result_presentation_view,
    build_result_tab_labels,
    build_selected_timeline_metric_options,
    build_simulation_table_rows,
    build_timeline_chart_rows,
    build_timeline_rows,
    selected_metric_ids_from_session as _selected_metric_ids_from_session,
)
from frontend.features.simulation.components.events import (
    build_overview_event_legend_rows,
    build_timeline_event_flag_rows,
    render_event_icon_legend,
    render_profile_event_legend,
)
from frontend.features.simulation.utils.helpers import (
    METRIC_TIMELINE_COLORS,
    PROFILE_TIMELINE_COLORS,
    TIMELINE_METRIC_LABELS,
    latest_timeline_item_by_step as _latest_timeline_item_by_step,
    step_short_label as _step_short_label,
    step_sort_value as _step_sort_value,
)
from frontend.features.simulation.components.insights import (
    build_profile_recommendation_cards,
    render_profile_explainable_cards,
)
from frontend.features.simulation.components.legends import (
    render_overview_result_context,
)
from frontend.features.simulation.components.summary import (
    render_profile_comparison_report,
    render_result_section_heading,
)


DYNAMIC_STATE_METRICS = (
    ("attention", "Aufmerksamkeit"),
    ("fatigue", "Ermüdung"),
    ("reading_speed", "Lesegeschwindigkeit"),
    ("progress_rate", "Fortschrittsrate"),
)

RESULT_TAB_STATE_KEY = "simulation_result_active_tab"
RESULT_SCROLL_TARGET_KEY = "simulation_result_scroll_target"


def _format_duration(seconds: float | int | None) -> str:
    total_seconds = max(0, int(round(float(seconds or 0))))
    minutes, remaining_seconds = divmod(total_seconds, 60)
    if minutes:
        return f"{minutes} Min. {remaining_seconds} Sek."
    return f"{remaining_seconds} Sek."


def _event_count(profile: dict) -> int:
    events = profile.get("display_events") or profile.get("events") or []
    if events:
        return len(events)
    return sum(
        len(item.get("events", []))
        for item in profile.get("display_timeline", profile.get("timeline", []))
    )


def _profile_recommendation_count(profile: dict) -> int:
    return len(profile.get("recommendation_cards") or [])


def _profile_priority_counts(profile: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for card in profile.get("recommendation_cards") or []:
        priority = str(card.get("priority") or "normal").strip().lower()
        counts[priority] = counts.get(priority, 0) + 1
    return counts


def _set_result_profile_target(profile_label: str, profile_id: str) -> None:
    st.session_state[RESULT_TAB_STATE_KEY] = profile_label
    st.session_state[RESULT_SCROLL_TARGET_KEY] = profile_id


def _priority_rank(priority: str) -> int:
    return {"hoch": 0, "mittel": 1, "niedrig": 2}.get(priority, 3)


def _highest_priority_label(cards: list[dict]) -> str:
    priorities = [
        str(card.get("priority") or "").strip().lower()
        for card in cards
        if card.get("priority")
    ]
    if not priorities:
        return "kein dringender Anpassungsbedarf"
    return sorted(priorities, key=_priority_rank)[0]


def _priority_filter_options(cards: list[dict]) -> list[str]:
    priorities = {
        str(card.get("priority") or "").strip().lower()
        for card in cards
        if card.get("priority")
    }
    ordered = []
    for priority, label in (
        ("hoch", "Hoch"),
        ("mittel", "Mittel"),
        ("niedrig", "Niedrig"),
    ):
        if priority in priorities or (priority == "niedrig" and "low" in priorities):
            ordered.append(label)
    return ["Alle", *ordered]


def _filter_recommendation_cards_by_priority(
    cards: list[dict],
    selected_priority: str,
) -> list[dict]:
    normalized = selected_priority.strip().lower()
    if normalized == "alle":
        return cards
    accepted_priorities = {"low", "niedrig"} if normalized == "niedrig" else {normalized}
    return [
        card
        for card in cards
        if str(card.get("priority") or "").strip().lower() in accepted_priorities
    ]


def _rounded_time_axis_end(max_seconds: float) -> int:
    padded_seconds = max_seconds + max(15.0, max_seconds * 0.12)
    if padded_seconds <= 60:
        return int(math.ceil(padded_seconds / 10) * 10)
    if padded_seconds <= 180:
        return int(math.ceil(padded_seconds / 30) * 30)
    return int(math.ceil(padded_seconds / 60) * 60)


def _overview_step_markup(affected_step: str) -> str:
    text = " ".join(str(affected_step or "").strip().split())
    if not text:
        return ""
    match = re.match(r"^(Step\s+\d+)\s*[–-]\s*(.+)$", text)
    if match:
        step_number = match.group(1)
        step_description = match.group(2)
    else:
        step_number = "Schritt"
        step_description = text
    return (
        '<div class="cogsim-overview-recommendation-step">'
        f'<span>{escape(step_number)}</span>'
        f'<p>{escape(step_description)}</p>'
        "</div>"
    )


def render_metric_step_timeline(
    rows: list[dict],
    event_rows: list[dict],
    *,
    color_field: str,
    color_title: str,
    height: int = 340,
) -> None:
    if not rows:
        st.caption("Keine Timeline-Daten vorhanden.")
        return

    step_sort = [
        step
        for step, _ in sorted(
            {row["Step"]: row["Step Order"] for row in rows}.items(),
            key=lambda item: item[1],
        )
    ]
    color_domain = []
    for row in rows:
        value = row.get(color_field, "")
        if value and value not in color_domain:
            color_domain.append(value)
    color_range = (
        PROFILE_TIMELINE_COLORS
        if color_field == "Profil"
        else METRIC_TIMELINE_COLORS
    )
    line_chart = (
        alt.Chart(alt.Data(values=rows))
        .mark_line(
            point={"filled": True, "size": 58},
            strokeWidth=2.6,
            interpolate="monotone",
        )
        .encode(
            x=alt.X(
                "Step:N",
                title="Aufgabenschritte",
                sort=step_sort,
                axis=alt.Axis(
                    labelAngle=0,
                    labelColor="#6B7280",
                    labelFontSize=12,
                    labelFontWeight=600,
                    titleFontSize=12,
                    titleColor="#6B7280",
                    titleFontWeight=600,
                    titlePadding=12,
                ),
            ),
            y=alt.Y(
                "Wert:Q",
                title="Wert (0–100)",
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(
                    values=[0, 20, 40, 60, 80, 100],
                    grid=True,
                    gridColor="#EEF2F7",
                    gridOpacity=1,
                    domain=False,
                    tickColor="#E5E7EB",
                    labelColor="#6B7280",
                    labelFontSize=12,
                    labelFontWeight=600,
                    titleFontSize=12,
                    titleColor="#6B7280",
                    titleFontWeight=600,
                    titlePadding=12,
                ),
            ),
            color=alt.Color(
                f"{color_field}:N",
                title=color_title,
                scale=alt.Scale(
                    domain=color_domain,
                    range=list(color_range)[: len(color_domain)],
                ),
                legend=alt.Legend(
                    orient="bottom",
                    direction="horizontal",
                    columns=max(1, len(color_domain)),
                    title=None,
                    labelColor="#4B4663",
                    labelFontSize=12,
                    labelFontWeight=600,
                    symbolSize=120,
                    symbolStrokeWidth=4,
                    labelLimit=220,
                ),
            ),
            tooltip=[
                alt.Tooltip("Step:N", title="Arbeitsschritt"),
                alt.Tooltip("Step Detail:N", title="Was passiert hier?"),
                alt.Tooltip("Profil:N", title="Profil"),
                alt.Tooltip("Metrik:N", title="Wert"),
                alt.Tooltip("Wert:Q", title="Wert", format=".1f"),
            ],
        )
    )
    chart = line_chart
    visible_event_rows = [
        row for row in event_rows if row.get("Step") in set(step_sort)
    ]
    if visible_event_rows:
        event_markers = (
            alt.Chart(alt.Data(values=visible_event_rows))
            .mark_text(
                align="center",
                baseline="top",
                dy=0,
                fontSize=14,
                fontWeight=700,
                color="#7C4DFF",
                opacity=0.9,
                clip=False,
            )
            .encode(
                x=alt.X("Step:N", sort=step_sort),
                y=alt.value(8),
                text=alt.Text("Event Symbols:N"),
                tooltip=[
                    alt.Tooltip("Profil:N", title="Profil"),
                    alt.Tooltip("Step:N", title="Arbeitsschritt"),
                    alt.Tooltip("Step Detail:N", title="Was passiert hier?"),
                    alt.Tooltip("Event Tooltip:N", title="Event-Marker"),
                ],
            )
        )
        chart = chart + event_markers

    st.altair_chart(
        chart.properties(
            height=height,
            padding={"left": 4, "right": 10, "top": 12, "bottom": 4},
        )
        .configure_view(stroke=None)
        .configure_axis(labelFont="Inter, system-ui, sans-serif")
        .configure_legend(labelFont="Inter, system-ui, sans-serif"),
        use_container_width=True,
    )
    render_event_icon_legend(visible_event_rows)


def render_overview_metric_timeline(
    profiles: list[dict],
    presentation: dict | None = None,
) -> None:
    with st.container(key="simulation_timeline_panel_overview"):
        render_result_section_heading(presentation or {}, "timeline")
        metric_options = build_selected_timeline_metric_options(
            profiles,
            _selected_metric_ids_from_session(),
        )
        if not metric_options:
            st.caption(
                "Für die ausgewählten Werte ist kein Verlauf über die "
                "Arbeitsschritte vorhanden."
            )
            return

        default_index = next(
            (
                index
                for index, option in enumerate(metric_options)
                if option["id"] == "error_risk"
            ),
            0,
        )
        selected_label = st.selectbox(
            "Wert auswählen",
            [option["label"] for option in metric_options],
            index=default_index,
            key="simulation_result_metric_filter",
        )
        selected_metric = next(
            option["id"]
            for option in metric_options
            if option["label"] == selected_label
        )
        render_metric_step_timeline(
            build_overview_metric_timeline_rows(profiles, selected_metric),
            build_timeline_event_flag_rows(profiles, presentation),
            color_field="Profil",
            color_title="Profil",
        )


def render_profile_metric_timeline(
    profile: dict,
    presentation: dict | None = None,
) -> None:
    with st.container(key=f"simulation_timeline_panel_{profile['profile_id']}"):
        render_result_section_heading(presentation or {}, "timeline")
        metric_options = build_selected_timeline_metric_options(
            [profile],
            _selected_metric_ids_from_session(),
        )
        rows = build_profile_metric_timeline_rows(
            profile,
            [option["id"] for option in metric_options],
        )
        render_metric_step_timeline(
            rows,
            build_timeline_event_flag_rows([profile], presentation),
            color_field="Metrik",
            color_title="Metrik",
        )


def build_profile_state_timeline_rows(profile: dict) -> list[dict]:
    rows = []
    for item in _latest_timeline_item_by_step(profile.get("timeline", [])):
        task_step = item.get("current_task_step", {})
        for metric_id, label in DYNAMIC_STATE_METRICS:
            if metric_id == "progress_rate":
                value = task_step.get("progress_rate")
            else:
                value = item.get(metric_id)
            if not isinstance(value, int | float):
                continue
            rows.append(
                {
                    "Profil": profile["profile_label"],
                    "Metrik": label,
                    "Metric ID": metric_id,
                    "Step": _step_short_label(task_step),
                    "Step Detail": task_step_display_label(task_step),
                    "Step Order": _step_sort_value(task_step),
                    "Wert": max(0, min(float(value), 100)),
                }
            )
    return rows


def render_profile_state_timeline(
    profile: dict,
    presentation: dict | None = None,
) -> None:
    rows = build_profile_state_timeline_rows(profile)
    if not rows:
        return
    with st.container(key=f"simulation_state_panel_{profile['profile_id']}"):
        st.markdown(
            """
            <div class="cogsim-result-section-copy">
                <h4>Simulationszustände</h4>
                <p>Diese Werte verändern sich während der Simulation. Sie zeigen,
                wie Aufmerksamkeit, Ermüdung, Lesegeschwindigkeit und Fortschritt
                im Aufgabenverlauf reagieren.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_metric_step_timeline(
            rows,
            build_timeline_event_flag_rows([profile], presentation),
            color_field="Metrik",
            color_title="Zustand",
            height=250,
        )


def render_overview_time_comparison(profiles: list[dict]) -> None:
    if not profiles:
        return
    sorted_profiles = sorted(
        profiles,
        key=lambda profile: float(profile.get("completion_time_seconds") or 0),
        reverse=True,
    )
    slowest_profile = sorted_profiles[0]
    chart_rows = [
        {
            "Profil": profile["profile_label"],
            "Bearbeitungszeit (s)": float(profile.get("completion_time_seconds") or 0),
        }
        for profile in sorted_profiles
    ]
    axis_end = _rounded_time_axis_end(
        max(row["Bearbeitungszeit (s)"] for row in chart_rows) if chart_rows else 1
    )
    cards = []
    for index, profile in enumerate(sorted_profiles):
        is_slowest = profile["profile_id"] == slowest_profile["profile_id"]
        cards.append(
            (
                '<article class="cogsim-overview-time-profile '
                f'{"cogsim-overview-time-profile--primary" if is_slowest else ""}">'
                f'<span>{escape(profile["profile_label"])}</span>'
                f'<strong>{escape(_format_duration(profile.get("completion_time_seconds")))}</strong>'
                f'<small>{"langsamstes Profil" if is_slowest else "simulierte Bearbeitungszeit"}</small>'
                "</article>"
            )
        )
    bars = (
        alt.Chart(alt.Data(values=chart_rows))
        .mark_bar(cornerRadiusTopRight=9, cornerRadiusBottomRight=9)
        .encode(
            y=alt.Y(
                "Profil:N",
                sort=[row["Profil"] for row in chart_rows],
                title=None,
                axis=alt.Axis(
                    labelColor="#4B4663",
                    labelFontSize=12,
                    labelFontWeight=600,
                ),
            ),
            x=alt.X(
                "Bearbeitungszeit (s):Q",
                title="Sekunden",
                scale=alt.Scale(domain=[0, axis_end], nice=False),
                axis=alt.Axis(
                    grid=True,
                    gridColor="#EEF2F7",
                    domain=True,
                    domainColor="#CBD5E1",
                    domainWidth=1.2,
                    labelColor="#6B7280",
                    labelFontSize=11,
                    titleColor="#6B7280",
                    titleFontSize=11,
                    titleFontWeight=600,
                ),
            ),
            color=alt.Color(
                "Profil:N",
                legend=None,
                scale=alt.Scale(
                    domain=[row["Profil"] for row in chart_rows],
                    range=list(PROFILE_TIMELINE_COLORS)[: len(chart_rows)],
                ),
            ),
            tooltip=[
                alt.Tooltip("Profil:N", title="Profil"),
                alt.Tooltip(
                    "Bearbeitungszeit (s):Q",
                    title="Bearbeitungszeit",
                    format=".0f",
                ),
            ],
        )
    )
    axis_rules = (
        alt.Chart(
            alt.Data(
                values=[
                    {"Grenze": 0},
                    {"Grenze": axis_end},
                ]
            )
        )
        .mark_rule(
            color="#CBD5E1",
            strokeWidth=1.2,
        )
        .encode(
            x=alt.X(
                "Grenze:Q",
                scale=alt.Scale(domain=[0, axis_end], nice=False),
            )
        )
    )
    st.markdown(
        (
            '<section class="cogsim-overview-time-panel">'
            '<div class="cogsim-overview-time-panel__header">'
            "<span>Bearbeitungszeiten</span>"
            "<p>Der erste Vergleich zeigt, welches Profil für dieselbe Aufgabe "
            "am längsten braucht.</p>"
            "</div>"
            '<div class="cogsim-overview-time-grid">'
            + "".join(cards)
            + "</div>"
            "</section>"
        ),
        unsafe_allow_html=True,
    )
    st.altair_chart(
        (axis_rules + bars)
        .properties(height=190)
        .configure_view(stroke=None)
        .configure_axis(labelFont="Inter, system-ui, sans-serif"),
        use_container_width=True,
    )


def render_overview_recommendation_summary(profiles: list[dict]) -> None:
    st.markdown(
        (
            '<section class="cogsim-overview-recommendation-summary">'
            '<div class="cogsim-result-section-heading">'
            "<span>Handlungsempfehlungen</span>"
            "<small>Die Übersicht zeigt nur, wo Anpassungsbedarf besteht. "
            "Die vollständige Begründung findest du in den Profilseiten.</small>"
            "</div>"
            "</section>"
        ),
        unsafe_allow_html=True,
    )
    columns = st.columns(max(1, len(profiles)))
    for column, profile in zip(columns, profiles):
        cards = build_profile_recommendation_cards(profile)
        titles = [
            str(card.get("title") or "Empfehlung").strip()
            for card in cards[:2]
            if card.get("title")
        ]
        preview_items = "".join(
            f"<li>{escape(title)}</li>" for title in titles
        ) or "<li>Kein dringender Anpassungsbedarf erkannt.</li>"
        affected_step = next(
            (
                str(card.get("affected_step") or "").strip()
                for card in cards
                if card.get("affected_step")
            ),
            "",
        )
        step_hint = _overview_step_markup(affected_step)
        with column:
            st.markdown(
                (
                    '<article class="cogsim-overview-recommendation-preview">'
                    f'<div><strong>{escape(profile["profile_label"])}</strong>'
                    f'<span>{_profile_recommendation_count(profile)} Empfehlungen</span></div>'
                    f'<small>höchste Priorität: {escape(_highest_priority_label(cards))}</small>'
                    f"<ul>{preview_items}</ul>"
                    f"{step_hint}"
                    "</article>"
                ),
                unsafe_allow_html=True,
            )
            st.button(
                "Empfehlungen ansehen",
                key=f"result_recommendation_jump_{profile['profile_id']}",
                on_click=_set_result_profile_target,
                args=(profile["profile_label"], profile["profile_id"]),
                width="stretch",
            )


def build_simulation_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def build_simulation_export(result: dict, workflow_state: dict) -> dict:
    simulation_results = result.get("simulation_results") or workflow_state.get(
        "simulation_results", {}
    )
    single_result = result.get("results", result)
    plan_profiles = {
        profile.get("profile_id"): profile.get("label")
        for profile in (
            workflow_state.get("simulation_plan", {}) or {}
        ).get("selected_user_profiles", [])
    }
    user_models = [
        {
            "profile_id": profile_id,
            "profile_label": plan_profiles.get(
                profile_id, model.get("user_type", profile_id)
            ),
            "attributes": {
                key: value
                for key, value in model.items()
                if key not in {"user_type", "assumptions"}
            },
            "assumptions": model.get("assumptions", []),
        }
        for profile_id, model in workflow_state.get("user_models", {}).items()
    ]
    return {
        "user_models": user_models,
        "task_model": workflow_state.get("task_model", {}),
        "interface_model": workflow_state.get("interface_model", {}),
        "environment_model": workflow_state.get("environment_model", {}),
        "computed_parameters": workflow_state.get("computed_parameters", {}),
        "simulation_results": simulation_results or single_result,
        "events": {
            profile_id: profile.get("events", [])
            for profile_id, profile in simulation_results.get(
                "results_by_profile", {}
            ).items()
        },
        "result_metrics": {
            profile_id: profile.get("final_metrics", {})
            for profile_id, profile in simulation_results.get(
                "results_by_profile", {}
            ).items()
        },
    }


def render_compact_timeline(profile: dict) -> None:
    render_profile_metric_timeline(profile)


def render_profile_result(profile: dict, presentation: dict | None = None) -> None:
    if not profile.get("completed", True):
        st.error("Simulation abgebrochen")

    render_profile_metric_timeline(profile, presentation)
    st.write("")
    render_profile_state_timeline(profile, presentation)
    st.write("")
    render_profile_event_legend(profile, presentation)

    recommendation_cards = build_profile_recommendation_cards(profile)
    if recommendation_cards:
        anchor_id = f"cogsim-recommendations-{profile['profile_id']}"
        st.markdown(
            f'<span id="{escape(anchor_id)}"></span>',
            unsafe_allow_html=True,
        )
        if st.session_state.get(RESULT_SCROLL_TARGET_KEY) == profile["profile_id"]:
            components.html(
                f"""
                <script>
                    const target = window.parent.document.getElementById("{anchor_id}");
                    if (target) {{
                        setTimeout(() => target.scrollIntoView({{
                            behavior: "smooth",
                            block: "start"
                        }}), 120);
                    }}
                </script>
                """,
                height=0,
            )
            st.session_state[RESULT_SCROLL_TARGET_KEY] = None
        st.markdown("#### Konkrete Handlungsempfehlungen")
        with st.container(key=f"recommendation_priority_filter_{profile['profile_id']}"):
            selected_priority = st.radio(
                "Empfehlungen nach Priorität filtern",
                _priority_filter_options(recommendation_cards),
                horizontal=True,
                key=f"recommendation_priority_{profile['profile_id']}",
            )
        filtered_recommendation_cards = _filter_recommendation_cards_by_priority(
            recommendation_cards,
            selected_priority,
        )
        if not filtered_recommendation_cards:
            st.info("Für diese Priorität gibt es keine Empfehlungen.")
            return
        render_profile_explainable_cards(
            "Empfehlung",
            filtered_recommendation_cards,
            tone="recommendation",
        )


def render_simulation_results(result: dict) -> None:
    profiles = build_display_profile_views(result)
    presentation = build_result_presentation_view(result)
    rows = build_simulation_table_rows(result)
    if not profiles:
        st.info("No simulation logs available.")
        return

    tab_labels = build_result_tab_labels(profiles)
    if st.session_state.get(RESULT_TAB_STATE_KEY) not in tab_labels:
        st.session_state[RESULT_TAB_STATE_KEY] = tab_labels[0]

    with st.container(key="result_navigation_tabs"):
        active_tab = st.radio(
            "Ergebnisbereich",
            tab_labels,
            horizontal=True,
            label_visibility="collapsed",
            key=RESULT_TAB_STATE_KEY,
        )

    if active_tab == tab_labels[0]:
        selected_metric_ids = _selected_metric_ids_from_session()
        render_overview_time_comparison(profiles)
        st.write("")
        render_result_section_heading(presentation, "profile_comparison")
        render_profile_comparison_report(profiles, selected_metric_ids)
        st.write("")
        render_overview_recommendation_summary(profiles)
        st.write("")
        render_overview_result_context(
            profiles,
            presentation,
            selected_metric_ids,
        )
    else:
        for profile in profiles:
            if active_tab == profile["profile_label"]:
                render_profile_result(profile, presentation)
                break

    st.divider()
    st.download_button(
        "Timeline als CSV exportieren",
        data=build_simulation_csv(rows),
        file_name="cogsim_simulation_timeline.csv",
        mime="text/csv",
        width="stretch",
    )

    export_data = build_simulation_export(
        result,
        st.session_state.get("backend_state", {}),
    )
    st.download_button(
        "Vollständige Ergebnisse als JSON exportieren",
        data=json.dumps(export_data, ensure_ascii=False, indent=2),
        file_name="cogsim_simulation_result.json",
        mime="application/json",
        width="stretch",
    )
