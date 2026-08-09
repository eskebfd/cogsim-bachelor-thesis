from collections import defaultdict

from backend.domains.simulation.schemas.recommendations import (
    RecommendationInterpretationContextView,
    RecommendationView,
    StructuredRecommendationView,
)


RECOMMENDATION_THRESHOLDS = {
    "minimum_absolute_delay_seconds": 5,
    "minimum_relative_delay": 0.25,
    "critical_attention": 45,
    "notable_attention": 60,
    "critical_reading_speed": 65,
    "notable_reading_speed": 75,
    "notable_cognitive_load": 65,
    "critical_cognitive_load": 75,
    "notable_error_risk": 55,
    "critical_error_risk": 70,
    "notable_fatigue": 60,
}

READING_OPERATIONS = {"read", "perceive"}
NAVIGATION_OPERATIONS = {"point", "click", "move", "perceive"}
INPUT_OPERATIONS = {"type", "keystroke", "input"}
DECISION_OPERATIONS = {"think", "decide", "choose", "compare"}

EVENT_LABELS = {
    "very_low_attention": "sehr niedrige Aufmerksamkeit",
    "very_high_cognitive_load": "hohe kognitive Belastung",
    "high_error_risk": "erhöhtes Fehlerrisiko",
    "rework_event": "Wiederholung/Korrektur",
    "time_pressure_warning": "Zeitdruck",
    "task_aborted": "Abbruch",
}

EVENT_TO_METRIC_IDS = {
    "very_low_attention": ["error_risk", "completion_time", "task_success_score"],
    "very_high_cognitive_load": ["cognitive_load", "error_risk", "task_success_score"],
    "high_error_risk": ["error_risk", "task_success_score"],
    "rework_event": ["completion_time", "completion_efficiency", "task_success_score"],
    "time_pressure_warning": ["time_limit_risk", "completion_time", "error_risk"],
    "task_aborted": ["task_success_score", "completion_efficiency", "completion_time"],
    "high_inhibition_load": ["cognitive_load", "error_risk"],
    "task_switching_strain": ["cognitive_load", "completion_time", "error_risk"],
}


def _number(value, default: float = 0.0) -> float:
    return float(value) if isinstance(value, int | float) else default


def _metric(metrics: dict, metric_id: str) -> float:
    if metric_id == "task_success_score":
        return _number(
            metrics.get("task_success_score", metrics.get("task_success_probability"))
        )
    return _number(metrics.get(metric_id))


def _step_label(step: dict) -> str:
    return step.get("display_name") or step.get("description") or step.get("name") or "Arbeitsschritt"


def _step_operations(step: dict) -> set[str]:
    operations = step.get("goms_operations") or step.get("operations") or []
    if isinstance(operations, str):
        operations = [operations]
    return {str(operation).lower() for operation in operations}


def _step_type(step: dict) -> str:
    return str(step.get("step_type") or "").lower()


def _is_reading_step(step: dict) -> bool:
    lowered = " ".join(
        str(step.get(key, "")).lower()
        for key in ("name", "description", "display_name")
    )
    return (
        _step_type(step) in {"read", "inspect", "review"}
        or bool(_step_operations(step) & READING_OPERATIONS)
        or any(word in lowered for word in ("lesen", "prüfen", "ansehen", "informationen", "text"))
    )


def _is_input_step(step: dict) -> bool:
    lowered = " ".join(
        str(step.get(key, "")).lower()
        for key in ("name", "description", "display_name")
    )
    return (
        _step_type(step) in {"input", "type", "form"}
        or bool(_step_operations(step) & INPUT_OPERATIONS)
        or any(word in lowered for word in ("eingeben", "formular", "feld", "absenden", "bestätigen", "buchung"))
    )


def _is_decision_step(step: dict) -> bool:
    lowered = " ".join(
        str(step.get(key, "")).lower()
        for key in ("name", "description", "display_name")
    )
    return (
        _step_type(step) in {"decision", "choose", "compare"}
        or bool(_step_operations(step) & DECISION_OPERATIONS)
        or any(word in lowered for word in ("auswählen", "vergleichen", "entscheiden", "option", "angebot"))
    )


def _is_navigation_step(step: dict) -> bool:
    lowered = " ".join(
        str(step.get(key, "")).lower()
        for key in ("name", "description", "display_name")
    )
    return (
        _step_type(step) in {"navigate", "click", "select"}
        or bool(_step_operations(step) & NAVIGATION_OPERATIONS)
        or any(word in lowered for word in ("klick", "button", "navigation", "karte", "öffnen", "auswählen"))
    )


def _rows_by_step(timeline: list[dict]) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = defaultdict(list)
    for item in timeline:
        step = item.get("current_task_step") or {}
        step_id = step.get("step_id") or str(step.get("step_index", 0))
        rows[str(step_id)].append(item)
    return rows


def _events_for_rows(rows: list[dict]) -> list[dict]:
    return [event for row in rows for event in row.get("events", [])]


def _event_types(events: list[dict]) -> set[str]:
    return {str(event.get("event_type")) for event in events}


def _event_labels(events: list[dict]) -> list[str]:
    labels = []
    for event in events:
        label = EVENT_LABELS.get(event.get("event_type"), event.get("event_type", "Event"))
        if label not in labels:
            labels.append(label)
    return labels


def _event_ids(events: list[dict]) -> list[str]:
    ids = []
    for event in events:
        event_type = str(event.get("event_type", ""))
        if event_type and event_type not in ids:
            ids.append(event_type)
    return ids


def _metric_ids_for_events(events: list[dict], fallback: list[str]) -> list[str]:
    metric_ids = []
    for event_id in _event_ids(events):
        for metric_id in EVENT_TO_METRIC_IDS.get(event_id, []):
            if metric_id not in metric_ids:
                metric_ids.append(metric_id)
    for metric_id in fallback:
        if metric_id not in metric_ids:
            metric_ids.append(metric_id)
    return metric_ids


def _ui_component_for_step(step: dict) -> str:
    if _is_input_step(step):
        return "Eingabe- oder Bestätigungselement"
    if _is_decision_step(step):
        return "Auswahl- oder Vergleichsbereich"
    if _is_navigation_step(step):
        return "Navigation oder nächster Handlungsschritt"
    if _is_reading_step(step):
        return "Text- oder Informationsbereich"
    return "betroffener Interface-Bereich"


def _structured_recommendation(
    *,
    step: dict,
    events: list[dict],
    fallback_metric_ids: list[str],
    cause: str,
    severity: str,
    design_principle: str,
    general_recommendation: str,
    priority: str,
    rule_id: str,
) -> StructuredRecommendationView:
    return StructuredRecommendationView(
        triggering_metric_ids=_metric_ids_for_events(events, fallback_metric_ids),
        triggering_event_ids=_event_ids(events),
        affected_task_step_id=str(step.get("step_id") or "") or None,
        affected_task_step_name=_step_label(step),
        affected_ui_component=_ui_component_for_step(step),
        cause=cause,
        severity=severity,
        design_principle=design_principle,
        general_recommendation=general_recommendation,
        priority=priority,
        rule_id=rule_id,
    )


def _with_interpretation_context(
    recommendation: RecommendationView,
) -> RecommendationView:
    recommendation.interpretation_context = RecommendationInterpretationContextView(
        must_not_change=[
            "triggering_metric_ids",
            "triggering_event_ids",
            "affected_task_step_id",
            "severity",
            "priority",
            "rule_id",
        ],
        structured_recommendation=recommendation.structured_recommendation,
    )
    return recommendation


def _step_stats(rows: list[dict]) -> dict[str, float]:
    if not rows:
        return {
            "min_attention": 100,
            "max_fatigue": 0,
            "max_cognitive_load": 0,
            "max_error_risk": 0,
            "min_reading_speed": 100,
        }
    return {
        "min_attention": min(_number(row.get("attention"), 100) for row in rows),
        "max_fatigue": max(_number(row.get("fatigue")) for row in rows),
        "max_cognitive_load": max(_number(row.get("cognitive_load")) for row in rows),
        "max_error_risk": max(_number(row.get("error_risk")) for row in rows),
        "min_reading_speed": min(_number(row.get("reading_speed"), 100) for row in rows),
    }


def _delay_values(step: dict) -> tuple[float, float, float]:
    planned = _number(step.get("planned_duration_seconds")) or _number(step.get("base_step_duration"))
    actual = _number(step.get("actual_duration_seconds")) or _number(step.get("actual_step_duration"))
    delay = max(0.0, actual - planned)
    relative = delay / planned if planned else 0.0
    return planned, actual, relative


def _is_significant_delay(step: dict) -> bool:
    planned, actual, relative = _delay_values(step)
    return (
        actual - planned >= RECOMMENDATION_THRESHOLDS["minimum_absolute_delay_seconds"]
        and relative >= RECOMMENDATION_THRESHOLDS["minimum_relative_delay"]
    )


HIGH_PRIORITY_EVENT_TYPES = {"task_aborted", "rework_event"}
STRONG_SIGNAL_EVENT_TYPES = {
    "high_error_risk",
    "very_high_cognitive_load",
    "very_low_attention",
    "high_inhibition_load",
    "task_switching_strain",
    "time_pressure_warning",
}


def _priority(
    *,
    critical: bool = False,
    event_count: int = 0,
    relative_delay: float = 0.0,
    event_types: set[str] | None = None,
) -> str:
    event_types = event_types or set()
    strong_event_count = len(event_types & STRONG_SIGNAL_EVENT_TYPES)
    if critical or event_types & HIGH_PRIORITY_EVENT_TYPES:
        return "hoch"
    if relative_delay >= 0.65:
        return "hoch"
    if strong_event_count >= 3:
        return "hoch"
    if strong_event_count >= 2 and relative_delay >= 0.35:
        return "hoch"
    if event_count >= 1 or relative_delay >= 0.25:
        return "mittel"
    return "niedrig"


def _confidence(evidence_count: int, has_event: bool) -> str:
    if has_event and evidence_count >= 3:
        return "hoch"
    if evidence_count >= 2:
        return "mittel"
    return "niedrig"


def _contextual_error_reasoning(
    *,
    profile_label: str,
    step: dict,
    stats: dict[str, float],
    events: list[dict],
) -> str:
    step_name = _step_label(step)
    event_hint = ""
    if events:
        event_hint = (
            " Zusätzlich wurden in diesem Schritt "
            f"{', '.join(_event_labels(events))} erkannt."
        )
    if _is_input_step(step):
        return (
            f"Der Schritt „{step_name}“ enthält wahrscheinlich eine Eingabe, "
            "Bestätigung oder andere fehlerkritische Aktion. Das erhöhte "
            f"Fehlerrisiko von {stats['max_error_risk']:.1f} von 100 bedeutet, "
            f"dass {profile_label} an dieser Stelle mehr Sicherheit und klarere "
            "Rückmeldung braucht, bevor die Handlung abgeschlossen wird."
            f"{event_hint}"
        )
    if _is_decision_step(step):
        return (
            f"Der Schritt „{step_name}“ verlangt vermutlich Vergleichen, Auswählen "
            "oder Abwägen mehrerer Optionen. Das erhöhte Fehlerrisiko deutet darauf "
            "hin, dass Unterschiede, Auswahlkriterien oder Folgen der Entscheidung "
            f"für {profile_label} nicht eindeutig genug sichtbar sind."
            f"{event_hint}"
        )
    if _is_reading_step(step):
        return (
            f"Der Schritt „{step_name}“ besteht vor allem aus dem Erfassen von "
            "Informationen. Wenn hier Fehlerrisiko entsteht, liegt die Hürde eher "
            "bei unklarer Textstruktur, schwer vergleichbaren Informationen oder "
            f"fehlender Orientierung als bei Formularfeldern. {profile_label} "
            "braucht an dieser Stelle eine leichter erfassbare Informationsführung."
            f"{event_hint}"
        )
    return (
        f"Im Schritt „{step_name}“ muss die nächste Handlung eindeutig erkennbar "
        f"sein. Das erhöhte Fehlerrisiko von {stats['max_error_risk']:.1f} von 100 "
        "spricht dafür, dass Beschriftungen, Status oder Rückmeldungen die Person "
        f"nicht ausreichend durch diesen Schritt führen.{event_hint}"
    )


def _contextual_fallback_actions(step: dict) -> list[str]:
    if _is_reading_step(step):
        primary_action = (
            "den Abschnitt mit einer klaren Zwischenüberschrift und einer kurzen "
            "Kernaussage einleiten"
        )
    elif _is_decision_step(step):
        primary_action = (
            "die wichtigsten Entscheidungskriterien direkt neben den Optionen sichtbar machen"
        )
    elif _is_input_step(step):
        primary_action = (
            "Pflichtfelder, aktuelle Auswahl und nächsten Schritt direkt am Eingabebereich erklären"
        )
    elif _is_navigation_step(step):
        primary_action = (
            "den nächsten erwarteten Klick durch Beschriftung, Position oder Hervorhebung klarer machen"
        )
    else:
        primary_action = (
            "die wichtigste Information und die nächste Handlung im Schritt sichtbarer hervorheben"
        )
    return [
        primary_action,
        "unnötige Zusatzinformationen in diesem Schritt reduzieren",
        "optional in einem kurzen Usability-Test beobachten, ob die Stelle weiterhin Unsicherheit auslöst",
    ]
