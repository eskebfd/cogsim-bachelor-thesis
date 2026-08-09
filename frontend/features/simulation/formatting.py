import re


VALUE_ALIASES = {
    "task_success_score": ("task_success_score", "task_success_probability"),
}

EVENT_DISPLAY_LABELS = {
    "very_low_attention": "Reduzierte Aufmerksamkeit",
    "very_high_cognitive_load": "Hohe kognitive Belastung",
    "high_error_risk": "Erhöhter Fehlerrisiko-Score",
    "time_pressure_warning": "Zeitdruck-Warnung",
    "rework_event": "Korrektur-/Wiederholungsschritt",
    "task_aborted": "Arbeitsschritt abgebrochen",

    "task_abandoned": "Arbeitsschritt abgebrochen",
}


def task_step_display_label(task_step: dict) -> str:
    step_index = task_step.get("step_index")
    if step_index is None:
        match = re.search(r"(\d+)$", str(task_step.get("step_id", "")))
        step_index = int(match.group(1)) - 1 if match else 0
    detail = task_step.get("description") or task_step.get("name", "")
    return f"Step {step_index + 1} – {detail}" if detail else f"Step {step_index + 1}"


def event_labels(events: list) -> str:
    labels = []
    for event in events:
        if isinstance(event, dict):
            event_type = event.get("event_type")
            label = (
                EVENT_DISPLAY_LABELS.get(event_type)
                if event_type
                else event.get("message", "")
            )
        else:
            label = str(event)
        if label:
            labels.append(label)
    return ", ".join(labels)


def number(value) -> str:
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".").replace(".", ",")
    return str(value)


def seconds(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    parts = str(value).split(":")
    try:
        return sum(
            float(part) * (60**index)
            for index, part in enumerate(reversed(parts))
        )
    except ValueError:
        return 0


def value_from_mapping(values: dict, key: str, default=0):
    for candidate in VALUE_ALIASES.get(key, (key,)):
        if candidate in values:
            return values.get(candidate, default)
    return default


def metric_value(profile: dict, key: str) -> float:
    value = value_from_mapping(profile.get("metrics", {}), key, 0)
    return value if isinstance(value, (int, float)) else 0


def step_duration_label(step: dict | None) -> str:
    if not step:
        return ""
    return (
        f"{step.get('display_name', '')} "
        f"({number(step.get('actual_duration_seconds', 0))} s)"
    )
