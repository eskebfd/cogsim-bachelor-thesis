METRIC_EVENT_RELATIONS = {
    "cognitive_load": [
        "very_high_cognitive_load",
        "high_inhibition_load",
        "task_switching_strain",
    ],
    "error_risk": [
        "high_error_risk",
        "very_high_cognitive_load",
        "very_low_attention",
        "time_pressure_warning",
        "rework_event",
        "high_inhibition_load",
        "task_switching_strain",
    ],
    "completion_time": [
        "very_high_cognitive_load",
        "very_low_attention",
        "rework_event",
        "time_pressure_warning",
        "task_aborted",
        "task_switching_strain",
    ],
    "completion_efficiency": [
        "very_low_attention",
        "rework_event",
        "task_aborted",
        "task_switching_strain",
    ],
    "task_success_score": [
        "high_error_risk",
        "very_high_cognitive_load",
        "very_low_attention",
        "rework_event",
        "task_aborted",
        "high_inhibition_load",
        "task_switching_strain",
    ],
    "time_limit_risk": ["time_pressure_warning"],
}


def event_ids_for_selected_metrics(
    selected_metric_ids: set[str] | None,
) -> set[str] | None:
    if selected_metric_ids is None:
        return None
    event_ids: set[str] = set()
    for metric_id in selected_metric_ids:
        event_ids.update(METRIC_EVENT_RELATIONS.get(metric_id, []))
    return event_ids
