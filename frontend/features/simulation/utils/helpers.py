from frontend.features.simulation.formatting import (
    seconds as _seconds,
    task_step_display_label,
    value_from_mapping as _value_from_mapping,
)


TIMELINE_METRICS = (
    ("attention", "Aufmerksamkeit"),
    ("fatigue", "Ermüdung"),
    ("cognitive_load", "Kognitive Belastung"),
    ("error_risk", "Fehlerrisiko"),
    ("reading_speed", "Lesegeschwindigkeit"),
    ("task_success_score", "Aufgabenerfolgswert"),
    ("completion_efficiency", "Bearbeitungseffizienz"),
)

TIMELINE_METRIC_LABELS = dict(TIMELINE_METRICS)
RESULT_METRIC_LABELS = {
    **TIMELINE_METRIC_LABELS,
    "completion_time": "Bearbeitungszeit",
    "time_limit_risk": "Zeitlimit-Risiko",
}
PROFILE_TIMELINE_COLORS = ("#4F46E5", "#D97706", "#059669", "#7C3AED")
METRIC_TIMELINE_COLORS = (
    "#5B5BD6",
    "#16A34A",
    "#EF4444",
    "#F59E0B",
    "#2563EB",
    "#7C3AED",
    "#6B7280",
)

PROFILE_COLOR_BY_ID = {
    "generic": "#4F46E5",
    "adhd": "#D97706",
    "dyslexie": "#059669",
    "dyslexia": "#059669",
}


def profile_color(profile: dict, fallback_index: int = 0) -> str:
    return PROFILE_COLOR_BY_ID.get(
        str(profile.get("profile_id", "")).lower(),
        PROFILE_TIMELINE_COLORS[fallback_index % len(PROFILE_TIMELINE_COLORS)],
    )


def bounded_metric_value(value) -> float:
    if not isinstance(value, int | float):
        return 0
    return max(0, min(float(value), 100))


def timeline_metric_value(item: dict, metric_id: str) -> float:
    if metric_id == "task_success_score":
        return bounded_metric_value(
            _value_from_mapping(item, "task_success_score", 0)
        )
    return bounded_metric_value(item.get(metric_id, 0))


def step_sort_value(task_step: dict) -> int:
    step_index = task_step.get("step_index")
    if isinstance(step_index, int):
        return step_index + 1
    step_id = str(task_step.get("step_id", ""))
    digits = "".join(character for character in step_id if character.isdigit())
    return int(digits) if digits else 1


def step_short_label(task_step: dict) -> str:
    return f"Step {step_sort_value(task_step)}"


def step_key(task_step: dict) -> str:
    return (
        str(task_step.get("step_id") or "")
        or str(task_step.get("name") or "")
        or task_step_display_label(task_step)
    )


def latest_timeline_item_by_step(timeline: list[dict]) -> list[dict]:
    by_step = {}
    for item in sorted(timeline, key=lambda row: _seconds(row.get("timestamp", 0))):
        task_step = item.get("current_task_step", {})
        by_step[step_key(task_step)] = item
    return sorted(
        by_step.values(),
        key=lambda row: step_sort_value(row.get("current_task_step", {})),
    )
