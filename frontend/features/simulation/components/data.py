import streamlit as st

from frontend.features.simulation.formatting import (
    event_labels as _event_labels,
    metric_value as _metric_value,
    seconds as _seconds,
    step_duration_label as _step_duration_label,
    task_step_display_label,
    value_from_mapping as _value_from_mapping,
)
from frontend.features.simulation.utils.helpers import (
    RESULT_METRIC_LABELS,
    TIMELINE_METRIC_LABELS,
    TIMELINE_METRICS,
    latest_timeline_item_by_step as _latest_timeline_item_by_step,
    step_short_label as _step_short_label,
    step_sort_value as _step_sort_value,
    timeline_metric_value as _timeline_metric_value,
)


RESULT_DURATION_KEYS = (
    "completion_time_seconds",
    "actual_processing_duration_seconds",
    "task_step_durations",
    "longest_task_step",
    "slowest_task_step",
    "fastest_task_step",
    "completed",
    "abort_reason",
    "aborted_step_id",
    "aborted_step_name",
    "allowed_step_duration",
    "actual_step_duration",
)


def _duration_values(profile_result: dict) -> dict:
    return {key: profile_result.get(key) for key in RESULT_DURATION_KEYS}


def build_profile_result_views(result: dict) -> list[dict]:
    multi_profile_result = result.get("simulation_results") or result
    results_by_profile = multi_profile_result.get("results_by_profile", {})
    return [
        {
            "profile_id": profile_id,
            "profile_label": profile_result.get("profile_label", profile_id),
            "metrics": profile_result.get("metrics")
            or profile_result.get("final_metrics", {}),
            "initial_state": profile_result.get("initial_user_state", {}),
            "final_state": profile_result.get(
                "final_state",
                profile_result.get("final_user_state", {}),
            ),
            "summary": profile_result.get("summary", {}),
            "events": profile_result.get("events", []),
            "display_events": profile_result.get(
                "display_events",
                profile_result.get("events", []),
            ),
            "timeline": profile_result.get("timeline", []),
            "display_timeline": profile_result.get(
                "display_timeline",
                profile_result.get("timeline", []),
            ),
            "is_baseline": profile_id
            == multi_profile_result.get("baseline_profile_id"),
            "problems": profile_result.get("problems", []),
            "recommendations": profile_result.get("recommendations", []),
            "recommendation_cards": profile_result.get(
                "recommendation_cards",
                [],
            ),
            "positive_findings": profile_result.get("positive_findings", []),
            **_duration_values(profile_result),
        }
        for profile_id, profile_result in results_by_profile.items()
    ]


def build_result_presentation_view(result: dict) -> dict:
    multi_profile_result = result.get("simulation_results") or result
    return multi_profile_result.get("result_presentation") or result.get(
        "result_presentation",
        {},
    )


def build_display_profile_views(result: dict) -> list[dict]:
    profiles = build_profile_result_views(result)
    if profiles:
        return profiles

    single_result = result.get("results", result)
    timeline = single_result.get("timeline") or result.get("logs", [])
    if not timeline:
        return []
    return [
        {
            "profile_id": single_result.get("profile_id", "generic"),
            "profile_label": single_result.get("profile_label", "Generic"),
            "metrics": single_result.get(
                "metrics",
                single_result.get("final_metrics", {}),
            ),
            "initial_state": single_result.get("initial_user_state", {}),
            "final_state": single_result.get(
                "final_state",
                single_result.get("final_user_state", {}),
            ),
            "summary": single_result.get("summary", {}),
            "events": single_result.get("events", []),
            "timeline": timeline,
            "is_baseline": True,
            "problems": single_result.get("problems", []),
            "recommendations": single_result.get("recommendations", []),
            "recommendation_cards": single_result.get(
                "recommendation_cards",
                [],
            ),
            "positive_findings": single_result.get("positive_findings", []),
            **_duration_values(single_result),
        }
    ]


def build_result_tab_labels(profiles: list[dict]) -> list[str]:
    return ["Überblick"] + [profile["profile_label"] for profile in profiles]


def build_timeline_rows(
    logs: list[dict],
    profile_id: str = "generic",
    profile_label: str = "Generic",
    completion_time_seconds: float = 0,
) -> list[dict]:
    return [
        {
            "Profile Label": profile_label,
            "Profile ID": profile_id,
            "Time": item.get("timestamp", ""),
            "Task Step": task_step_display_label(
                item.get("current_task_step", {})
            ),
            "Task Progress (%)": item.get("current_task_step", {}).get(
                "task_progress_percent", 0
            ),
            "Completion Time (s)": completion_time_seconds,
            "Reading Speed": item.get("reading_speed", 0),
            "Attention": item.get("attention", 0),
            "Fatigue": item.get("fatigue", 0),
            "Cognitive Load": item.get("cognitive_load", 0),
            "Error Risk Score": item.get("error_risk", 0),
            "Task Success Score": _value_from_mapping(item, "task_success_score", 0),
            "Completion Efficiency": item.get("completion_efficiency", 0),
            "Events": _event_labels(item.get("events", [])),
        }
        for item in logs
    ]


def build_simulation_table_rows(result: dict) -> list[dict]:
    profile_results = build_profile_result_views(result)
    if profile_results:
        return [
            row
            for profile in profile_results
            for row in build_timeline_rows(
                profile["timeline"],
                profile["profile_id"],
                profile["profile_label"],
                profile.get("completion_time_seconds", 0),
            )
        ]

    single_result = result.get("results", result)
    logs = single_result.get("timeline") or result.get("logs", [])
    profile_id = single_result.get("profile_id", "generic")
    profile_label = single_result.get("profile_label", "Generic")
    return build_timeline_rows(
        logs,
        profile_id,
        profile_label,
        single_result.get("completion_time_seconds", 0),
    )


def build_compact_timeline_rows(logs: list[dict]) -> list[dict]:
    return [
        {
            "Time": item.get("timestamp", ""),
            "Profile": item.get("profile_label") or item.get("profile", ""),
            "Task Step": task_step_display_label(
                item.get("current_task_step", {})
            ),
            "Task Progress (%)": round(item.get("task_progress", 0) * 100, 2),
            "Base Step Duration (s)": item.get("base_step_duration", 0),
            "Estimated Step Duration (s)": item.get(
                "actual_step_duration", 0
            ),
            "Attention": item.get("attention", 0),
            "Fatigue": item.get("fatigue", 0),
            "Cognitive Load": item.get("cognitive_load", 0),
            "Error Risk Score": item.get("error_risk", 0),
            "Events": _event_labels(item.get("events", [])),
        }
        for item in logs
    ]


def build_additional_timeline_rows(logs: list[dict]) -> list[dict]:
    return [
        {
            "Time": item.get("timestamp", ""),
            "Task Step": task_step_display_label(
                item.get("current_task_step", {})
            ),
            "Task Progress (%)": item.get("current_task_step", {}).get(
                "task_progress_percent", 0
            ),
            "Reading Speed": item.get("reading_speed", 0),
            "Task Success Score": _value_from_mapping(item, "task_success_score", 0),
            "Completion Efficiency": item.get("completion_efficiency", 0),
        }
        for item in logs
    ]


def build_profile_comparison_rows(profiles: list[dict]) -> list[dict]:
    rows = []
    for profile in profiles:
        state = profile.get("final_state", {})
        metrics = profile.get("metrics", {})
        event_count = len(profile.get("events", [])) or sum(
            len(item.get("events", []))
            for item in profile.get("timeline", [])
        )
        rows.append(
            {
                "Profil": profile["profile_label"],
                "Final Attention": state.get("attention", 0),
                "Final Fatigue": state.get("fatigue", 0),
                "Reading Speed": state.get("reading_speed", 0),
                "Cognitive Load": metrics.get("cognitive_load", 0),
                "Error Risk Score": metrics.get("error_risk", 0),
                "Task Success Score": _value_from_mapping(
                    metrics,
                    "task_success_score",
                    0,
                ),
                "Completion Efficiency": metrics.get(
                    "completion_efficiency", 0
                ),
                "Completion Time (s)": profile.get(
                    "completion_time_seconds", 0
                ),
                "Status": (
                    "Abgeschlossen"
                    if profile.get("completed", True)
                    else "Abgebrochen"
                ),
                "Abgebrochener Task Step": profile.get(
                    "aborted_step_name"
                ) or "",
                "Tatsächliche Bearbeitungsdauer (s)": profile.get(
                    "actual_processing_duration_seconds", 0
                ),
                "Längster Task Step": _step_duration_label(
                    profile.get("longest_task_step")
                ),
                "Langsamster Task Step": _step_duration_label(
                    profile.get("slowest_task_step")
                ),
                "Schnellster Task Step": _step_duration_label(
                    profile.get("fastest_task_step")
                ),
                "Anzahl Events": event_count,
            }
        )
    return rows


def build_event_summary_rows(profile: dict) -> list[dict]:
    events = profile.get("events", [])
    if not events:
        events = [
            event
            for item in profile.get("timeline", [])
            for event in item.get("events", [])
        ]
    event_counts = {}
    for event in events:
        event_type = event.get("event_type", "event")
        current = event_counts.setdefault(
            event_type,
            {
                "Event": event_type.replace("_", " ").title(),
                "Anzahl": 0,
                "Letzter Task Step": "",
            },
        )
        current["Anzahl"] += 1
        current["Letzter Task Step"] = (
            event.get("step_id")
            or event.get("task_step")
            or current["Letzter Task Step"]
        )
    return list(event_counts.values())


def build_notable_task_step_rows(profile: dict, limit: int = 3) -> list[dict]:
    by_step = {}
    for item in profile.get("timeline", []):
        task_step = item.get("current_task_step", {})
        step_id = task_step.get("step_id") or task_step.get("name", "")
        current = by_step.setdefault(
            step_id,
            {
                "Task Step": task_step_display_label(task_step),
                "Max. Cognitive Load": 0,
                "Max. Error Risk Score": 0,
                "Events": set(),
            },
        )
        current["Max. Cognitive Load"] = max(
            current["Max. Cognitive Load"], item.get("cognitive_load", 0)
        )
        current["Max. Error Risk Score"] = max(
            current["Max. Error Risk Score"], item.get("error_risk", 0)
        )
        current["Events"].update(
            event.get("event_type", "")
            for event in item.get("events", [])
            if event.get("event_type")
        )
    ranked = sorted(
        by_step.values(),
        key=lambda row: (
            bool(row["Events"]),
            row["Max. Error Risk Score"],
            row["Max. Cognitive Load"],
        ),
        reverse=True,
    )[:limit]
    return [
        {
            **row,
            "Events": ", ".join(sorted(row["Events"])),
        }
        for row in ranked
    ]


def build_overview_metric_chart_rows(profiles: list[dict]) -> list[dict]:
    rows = []
    for profile in profiles:
        rows.append(
            {
                "Profil": profile["profile_label"],
                "Cognitive Load": _metric_value(profile, "cognitive_load"),
                "Error Risk Score": _metric_value(profile, "error_risk"),
                "Task Success Score": _metric_value(
                    profile,
                    "task_success_score",
                ),
                "Completion Efficiency": _metric_value(
                    profile,
                    "completion_efficiency",
                ),
            }
        )
    return rows


def build_overview_duration_chart_rows(profiles: list[dict]) -> list[dict]:
    rows = []
    for profile in profiles:
        event_count = len(profile.get("events", [])) or sum(
            len(item.get("events", []))
            for item in profile.get("timeline", [])
        )
        rows.append(
            {
                "Profil": profile["profile_label"],
                "Completion Time (s)": profile.get(
                    "completion_time_seconds",
                    0,
                ),
                "Events": event_count,
            }
        )
    return rows


def build_metric_chart_rows(
    metrics: dict,
    selected_metric_ids: set[str] | None = None,
) -> list[dict]:
    return [
        {
            "Metrik": RESULT_METRIC_LABELS.get(
                key,
                key.replace("_", " ").title(),
            ),
            "Wert": value,
        }
        for key, value in metrics.items()
        if isinstance(value, int | float)
        and (
            selected_metric_ids is None
            or key in selected_metric_ids
            or (
                key == "task_success_probability"
                and "task_success_score" in selected_metric_ids
            )
        )
    ]


def build_timeline_chart_rows(logs: list[dict]) -> list[dict]:
    return [
        {
            "Time": item.get("timestamp", ""),
            "Attention": item.get("attention", 0),
            "Fatigue": item.get("fatigue", 0),
            "Cognitive Load": item.get("cognitive_load", 0),
            "Error Risk Score": item.get("error_risk", 0),
            "Reading Speed": item.get("reading_speed", 0),
        }
        for item in logs
    ]


def build_available_timeline_metric_options(profiles: list[dict]) -> list[dict]:
    options = []
    for metric_id, label in TIMELINE_METRICS:
        if any(
            any(
                metric_id in item
                or (
                    metric_id == "task_success_score"
                    and (
                        "task_success_score" in item
                        or "task_success_probability" in item
                    )
                )
                for item in profile.get("timeline", [])
            )
            for profile in profiles
        ):
            options.append({"id": metric_id, "label": label})
    return options


def selected_metric_ids_from_session() -> set[str] | None:
    evaluation_metrics = st.session_state.get("evaluation_metrics")
    backend_state = st.session_state.get("backend_state", {})

    if evaluation_metrics:
        return _metric_ids_from_selection(evaluation_metrics)

    if backend_state.get("evaluation_metrics"):
        return _metric_ids_from_selection(backend_state["evaluation_metrics"])

    if backend_state.get("simulation_plan"):
        return _metric_ids_from_selection(
            {
                "selected_metrics": backend_state["simulation_plan"].get(
                    "evaluation_metrics",
                    [],
                )
            }
        )

    return None


def _metric_ids_from_selection(selection: dict) -> set[str]:
    selected_ids = set()
    selected_metrics = selection.get("selected_metrics", [])
    for metric in selected_metrics:
        if isinstance(metric, str):
            selected_ids.add(metric)
        elif isinstance(metric, dict):
            metric_id = metric.get("metric_id") or metric.get("id")
            if metric_id:
                selected_ids.add(metric_id)
    if "task_success_probability" in selected_ids:
        selected_ids.add("task_success_score")
    return selected_ids


def build_selected_timeline_metric_options(
    profiles: list[dict],
    selected_metric_ids: set[str] | None,
) -> list[dict]:
    available_options = build_available_timeline_metric_options(profiles)
    if selected_metric_ids is None:
        return available_options
    return [
        option
        for option in available_options
        if option["id"] in selected_metric_ids
    ]


def build_profile_metric_timeline_rows(
    profile: dict,
    metric_ids: list[str] | None = None,
) -> list[dict]:
    rows = []
    selected_metric_ids = (
        [
            option["id"]
            for option in build_available_timeline_metric_options([profile])
        ]
        if metric_ids is None
        else metric_ids
    )
    for item in _latest_timeline_item_by_step(profile.get("timeline", [])):
        task_step = item.get("current_task_step", {})
        for metric_id in selected_metric_ids:
            if metric_id not in TIMELINE_METRIC_LABELS:
                continue
            rows.append(
                {
                    "Profil": profile["profile_label"],
                    "Metrik": TIMELINE_METRIC_LABELS[metric_id],
                    "Metric ID": metric_id,
                    "Step": _step_short_label(task_step),
                    "Step Detail": task_step_display_label(task_step),
                    "Step Order": _step_sort_value(task_step),
                    "Wert": _timeline_metric_value(item, metric_id),
                }
            )
    return rows


def build_overview_metric_timeline_rows(
    profiles: list[dict],
    metric_id: str,
) -> list[dict]:
    rows = []
    for profile in profiles:
        rows.extend(build_profile_metric_timeline_rows(profile, [metric_id]))
    return rows


def build_task_duration_chart_rows(profile: dict) -> list[dict]:
    return [
        {
            "Task Step": step["display_name"],
            "Geplant (s)": step["planned_duration_seconds"],
            "Tatsächlich (s)": step["actual_duration_seconds"],
            "Verzögerung (s)": step["delay_seconds"],
        }
        for step in profile.get("task_step_durations") or []
    ]
