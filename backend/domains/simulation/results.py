from statistics import fmean

from backend.domains.simulation.recommendations import (
    build_profile_recommendation_views,
)
from backend.domains.simulation.events.metric_relations import (
    event_ids_for_selected_metrics,
)
from backend.domains.simulation.presentation import (
    build_result_presentation_view,
)
from backend.domains.simulation.schemas.types import (
    MultiProfileSimulationResult,
    ProfileSimulationResult,
    ResultMetrics,
    UserState,
)

TASK_SUCCESS_SCORE_KEY = "task_success_score"
LEGACY_TASK_SUCCESS_PROBABILITY_KEY = "task_success_probability"


def task_success_score_value(values: dict, default: float = 0.0) -> float:
    value = values.get(
        TASK_SUCCESS_SCORE_KEY,
        values.get(LEGACY_TASK_SUCCESS_PROBABILITY_KEY, default),
    )
    return value if isinstance(value, (int, float)) else default


def task_step_display_name(task_step: dict) -> str:
    step_number = task_step.get("step_index", 0) + 1
    detail = task_step.get("description") or task_step.get("name", "")
    return f"Step {step_number} – {detail}" if detail else f"Step {step_number}"


def summarize_task_step_durations(timeline: list[dict]) -> list[dict]:
    steps = {}
    for item in timeline:
        task_step = item.get("current_task_step", {})
        step_id = task_step.get("step_id") or str(task_step.get("step_index", 0))
        current = steps.setdefault(
            step_id,
            {
                "step_id": step_id,
                "step_index": task_step.get("step_index", 0),
                "name": task_step.get("name", ""),
                "description": task_step.get("description", ""),
                "display_name": task_step_display_name(task_step),
                "step_type": task_step.get("step_type", ""),
                "goms_operations": task_step.get("goms_operations", []),
                "user_profile_id": item.get("profile"),
                "profile": item.get("profile"),
                "status": "completed",
                "abort_reason": None,
                "planned_duration_seconds": task_step.get(
                    "planned_duration_seconds",
                    task_step.get("duration_seconds", 0),
                ),
                "estimated_duration_seconds": task_step.get(
                    "estimated_duration_seconds",
                    task_step.get("duration_seconds", 0),
                ),
                "actual_duration_seconds": 0,
                "effective_duration_seconds": 0,
                "max_duration_seconds": task_step.get("max_duration_seconds"),
                "final_progress": 0.0,
                "slowdown_factor": 1.0,
            },
        )
        current["user_profile_id"] = item.get("profile")
        current["profile"] = item.get("profile")
        if task_step.get("status") == "aborted":
            current["status"] = "aborted"
            current["abort_reason"] = task_step.get("abort_reason")
        current["actual_duration_seconds"] = max(
            current["actual_duration_seconds"],
            task_step.get("elapsed_seconds", 0),
        )
        current["effective_duration_seconds"] = max(
            current["effective_duration_seconds"],
            task_step.get("effective_duration_seconds", 0),
        )
        current["slowdown_factor"] = max(
            current["slowdown_factor"],
            task_step.get("slowdown_factor", 1.0),
        )
        current["final_progress"] = max(
            current["final_progress"],
            task_step.get("final_progress", task_step.get("task_progress", 0)),
        )
        if task_step.get("max_duration_seconds") is not None:
            current["max_duration_seconds"] = task_step.get(
                "max_duration_seconds"
            )

    rows = sorted(steps.values(), key=lambda row: row["step_index"])
    for row in rows:
        planned = row["planned_duration_seconds"] or 1
        row["delay_seconds"] = max(
            0,
            row["actual_duration_seconds"] - row["planned_duration_seconds"],
        )
        row["duration_ratio"] = round(
            row["actual_duration_seconds"] / planned,
            2,
        )
        row["base_step_duration"] = row["planned_duration_seconds"]
        row["actual_step_duration"] = row["actual_duration_seconds"]
        row["max_step_duration"] = row["max_duration_seconds"]
        row["duration_modifier"] = row["duration_ratio"]
    return rows


def summarize_timeline(timeline: list[dict]) -> dict:
    """
    Erstellt aggregierte Kennzahlen über den gesamten Simulationsverlauf.
    """


    if not timeline:
        return {
            "average_cognitive_load": 0.0,
            "maximum_error_risk": 0.0,
            "average_task_success_score": 0.0,
            "average_completion_efficiency": 0.0,
            "event_count": 0,
        }


    return {
        "average_cognitive_load": round(
            fmean(item["cognitive_load"] for item in timeline),
            2,
        ),
        "maximum_error_risk": round(
            max(item["error_risk"] for item in timeline),
            2,
        ),
        "average_task_success_score": round(
            fmean(task_success_score_value(item) for item in timeline),
            2,
        ),
        "average_completion_efficiency": round(
            fmean(item["completion_efficiency"] for item in timeline),
            2,
        ),
        "event_count": sum(len(item["events"]) for item in timeline),
    }


def build_simulation_result(
    timeline: list[dict],
    initial_user_state: UserState,
    final_user_state: UserState,
    final_metrics: ResultMetrics | None,
    computed_task_parameters: dict[str, float],
    time_step_seconds: int,
    total_task_steps: int,
    simulation_model_used: bool = False,
    completed: bool = True,
    abort_reason: str | None = None,
    aborted_step_id: str | None = None,
    aborted_step_name: str | None = None,
    allowed_step_duration: float | None = None,
    actual_step_duration: float | None = None,
    time_limit_seconds: float | None = None,
) -> dict:
    """
    Erstellt das vollständige Simulationsergebnis, das an das
    Frontend zurückgegeben wird.
    """


    all_events = [
        {
            **event,
            "timestamp": item["timestamp"],
            "timestamp_seconds": item["timestamp_seconds"],
            "step_id": item["current_task_step"]["step_id"],
        }
        for item in timeline
        for event in item["events"]
    ]

    task_step_durations = summarize_task_step_durations(timeline)
    completion_time_seconds = (
        timeline[-1]["timestamp_seconds"] if timeline else 0
    )
    normalized_final_metrics = dict(final_metrics or {})
    if (
        TASK_SUCCESS_SCORE_KEY not in normalized_final_metrics
        and LEGACY_TASK_SUCCESS_PROBABILITY_KEY in normalized_final_metrics
    ):
        normalized_final_metrics[TASK_SUCCESS_SCORE_KEY] = normalized_final_metrics[
            LEGACY_TASK_SUCCESS_PROBABILITY_KEY
        ]
    normalized_final_metrics.pop(LEGACY_TASK_SUCCESS_PROBABILITY_KEY, None)
    report_metrics = {
        **normalized_final_metrics,
        "completion_time": completion_time_seconds,
        "time_limit_risk": (
            round(
                min(
                    100.0,
                    max(0.0, completion_time_seconds - time_limit_seconds)
                    / time_limit_seconds
                    * 100,
                ),
                2,
            )
            if time_limit_seconds
            else 0.0
        ),
    }
    longest_task_step = max(
        task_step_durations,
        key=lambda row: row["actual_duration_seconds"],
        default=None,
    )
    slowest_task_step = max(
        task_step_durations,
        key=lambda row: row["duration_ratio"],
        default=None,
    )
    fastest_task_step = min(
        task_step_durations,
        key=lambda row: row["actual_duration_seconds"],
        default=None,
    )
    (
        problems,
        recommendations,
        recommendation_cards,
        positive_findings,
    ) = build_profile_recommendation_views(
        profile_id="generic",
        profile_label="Das simulierte Profil",
        timeline=timeline,
        task_step_durations=task_step_durations,
        metrics=report_metrics,
        completed=completed and bool(timeline),
    )

    return {

        "completed": completed and bool(timeline),
        "status": "completed" if completed and bool(timeline) else "aborted",


        "abort_reason": abort_reason,
        "aborted_step_id": aborted_step_id,
        "aborted_step_name": aborted_step_name,
        "allowed_step_duration": allowed_step_duration,
        "actual_step_duration": actual_step_duration,
        "time_limit_seconds": time_limit_seconds,
        "time_step_seconds": time_step_seconds,
        "total_duration_seconds": completion_time_seconds,
        "completion_time_seconds": completion_time_seconds,
        "completion_time": completion_time_seconds,
        "actual_processing_duration_seconds": completion_time_seconds,
        "task_step_durations": task_step_durations,
        "aborted_steps": [
            row for row in task_step_durations if row.get("status") == "aborted"
        ],
        "longest_task_step": longest_task_step,
        "slowest_task_step": slowest_task_step,
        "fastest_task_step": fastest_task_step,
        "total_task_steps": total_task_steps,
        "total_timeline_entries": len(timeline),
        "simulation_model_used": simulation_model_used,

        "computed_task_parameters": computed_task_parameters,

        "initial_user_state": initial_user_state,
        "final_user_state": final_user_state,

        "final_metrics": report_metrics,

        "summary": summarize_timeline(timeline),

        "events": all_events,
        "problems": problems,
        "recommendations": recommendations,
        "recommendation_cards": recommendation_cards,
        "positive_findings": positive_findings,

        "timeline": timeline,

        "logs": timeline,

        "model_basis": {
            "architecture": [
                "basis_attributes",
                "computed_task_parameters",
                "user_state",
                "result_metrics",
            ],
            "user_state": [
                "reading_speed",
                "attention",
                "fatigue",
            ],
            "result_metrics": [
                "cognitive_load",
                "error_risk",
                "task_success_score",
                "completion_efficiency",
                "completion_time",
                "time_limit_risk",
            ],
            "update_model": ("weighted_linear_targets_with_linear_transition"),
        },

        "calibration_notes": [
            (
                "Die Gewichte folgen zunächst den gleich gewichteten "
                "Beispielen der Modellbeschreibung."
            ),
            (
                "Die zeitlichen Response-Raten sind austauschbare "
                "Annahmen und müssen empirisch kalibriert werden."
            ),
        ],
    }


def build_profile_simulation_result(
    profile_id: str,
    profile_label: str,
    user_model: dict,
    simulation_result: dict,
) -> ProfileSimulationResult:
    (
        problems,
        recommendations,
        recommendation_cards,
        positive_findings,
    ) = build_profile_recommendation_views(
        profile_id=profile_id,
        profile_label=profile_label,
        timeline=simulation_result.get("timeline", []),
        task_step_durations=simulation_result.get("task_step_durations", []),
        metrics=simulation_result.get("final_metrics", {}),
        completed=simulation_result.get("completed", True),
    )
    return {
        **simulation_result,
        "profile_id": profile_id,
        "profile_label": profile_label,
        "user_model": user_model,
        "final_state": simulation_result.get("final_user_state", {}),
        "metrics": simulation_result.get("final_metrics", {}),
        "problems": problems,
        "recommendations": recommendations,
        "recommendation_cards": recommendation_cards,
        "positive_findings": positive_findings,
    }


def _filtered_events_for_metrics(
    events: list[dict],
    selected_metric_ids: set[str] | None,
) -> list[dict]:
    allowed_event_ids = event_ids_for_selected_metrics(selected_metric_ids)
    if allowed_event_ids is None:
        return list(events)
    return [
        event
        for event in events
        if event.get("event_type") in allowed_event_ids
    ]


def _filtered_recommendation_cards_for_metrics(
    recommendation_cards: list[dict],
    selected_metric_ids: set[str] | None,
) -> list[dict]:
    if selected_metric_ids is None:
        return list(recommendation_cards)
    filtered_cards = []
    for card in recommendation_cards:
        structured = card.get("structured_recommendation") or {}
        metric_ids = set(structured.get("triggering_metric_ids") or [])
        if not metric_ids or metric_ids & selected_metric_ids:
            filtered_cards.append(card)
    return filtered_cards


def _attach_display_events(
    profile_results: list[ProfileSimulationResult],
    selected_metric_ids: set[str] | None,
) -> list[ProfileSimulationResult]:
    enriched_profiles = []
    for profile in profile_results:
        display_timeline = []
        for item in profile.get("timeline", []):
            display_timeline.append(
                {
                    **item,
                    "events": _filtered_events_for_metrics(
                        item.get("events", []),
                        selected_metric_ids,
                    ),
                }
            )
        display_events = _filtered_events_for_metrics(
            profile.get("events", []),
            selected_metric_ids,
        )
        display_recommendation_cards = _filtered_recommendation_cards_for_metrics(
            profile.get("recommendation_cards", []),
            selected_metric_ids,
        )
        enriched_profiles.append(
            {
                **profile,
                "raw_recommendation_cards": profile.get("recommendation_cards", []),
                "recommendation_cards": display_recommendation_cards,
                "display_events": display_events,
                "display_timeline": display_timeline,
            }
        )
    return enriched_profiles


def derive_profile_insights(
    profile_label: str,
    timeline: list[dict],
) -> tuple[list[str], list[str]]:
    if not timeline:
        return [], []
    task_step_durations = summarize_task_step_durations(timeline)
    summary = summarize_timeline(timeline)
    metrics = {
        "cognitive_load": summary["average_cognitive_load"],
        "error_risk": summary["maximum_error_risk"],
        "task_success_score": summary["average_task_success_score"],
        "completion_efficiency": summary["average_completion_efficiency"],
    }
    problems, recommendations, _, _ = build_profile_recommendation_views(
        profile_id="legacy",
        profile_label=profile_label,
        timeline=timeline,
        task_step_durations=task_step_durations,
        metrics=metrics,
    )
    return problems, recommendations


def build_simulation_results(
    profile_results: list[ProfileSimulationResult],
    baseline_profile_id: str | None = None,
    selected_metric_ids: set[str] | None = None,
) -> MultiProfileSimulationResult:
    profile_results = _attach_display_events(profile_results, selected_metric_ids)
    profile_ids = [result["profile_id"] for result in profile_results]
    resolved_baseline_id = (
        baseline_profile_id
        if baseline_profile_id in profile_ids
        else (profile_ids[0] if profile_ids else None)
    )
    problems = list(
        dict.fromkeys(
            problem
            for result in profile_results
            for problem in result.get("problems", [])
        )
    )
    recommendations = list(
        dict.fromkeys(
            recommendation
            for result in profile_results
            for recommendation in result.get("recommendations", [])
        )
    )
    result = {
        "completed": bool(profile_results)
        and all(result.get("completed", False) for result in profile_results),
        "profile_count": len(profile_results),
        "profile_ids": profile_ids,
        "baseline_profile_id": resolved_baseline_id,
        "results_by_profile": {
            result["profile_id"]: result for result in profile_results
        },
        "runs": profile_results,
        "comparison_summary": {
            "problems": problems,
            "recommendations": recommendations,
        },
    }
    if profile_results:
        result["result_presentation"] = build_result_presentation_view(
            profile_results,
            selected_metric_ids=selected_metric_ids,
        )
    return result
