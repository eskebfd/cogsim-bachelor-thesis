from backend.domains.evaluation.schemas.evaluation_metrics import (
    EvaluationMetricDefinition,
    EvaluationMetricsSelection,
)


_PREDEFINED_EVALUATION_METRICS = (
    EvaluationMetricDefinition(
        metric_id="cognitive_load",
        name="Kognitive Belastung",
        description=(
            "Modellierte mentale Beanspruchung während der Aufgabenbearbeitung "
            "auf einer Skala von 0 bis 100."
        ),
        metric_type="score",
        source="predefined",
        analysis_question="Wie hoch ist die kognitive Belastung im Verlauf?",
        data_basis="Task-, Text-, Navigations- und Fatigue-Werte",
        limitation="Heuristischer Belastungsscore, kein klinischer Messwert.",
        expected_output_range=(0, 100),
        higher_is_better=False,
        tags=["cognition", "workload"],
    ),
    EvaluationMetricDefinition(
        metric_id="error_risk",
        name="Fehlerrisiko",
        description=(
            "Heuristischer Risikoscore für fehlerhafte Interaktionen "
            "auf einer Skala von 0 bis 100; nicht empirisch kalibriert."
        ),
        metric_type="score",
        source="predefined",
        analysis_question="Bei welchen Schritten ist das Fehlerrisiko erhöht?",
        data_basis="Cognitive Load, Fatigue, Time Pressure und Attention",
        limitation="Risikowert, keine empirisch kalibrierte Wahrscheinlichkeit.",
        expected_output_range=(0, 100),
        higher_is_better=False,
        tags=["error", "risk"],
    ),
    EvaluationMetricDefinition(
        metric_id="completion_efficiency",
        name="Bearbeitungseffizienz",
        description=(
            "Heuristischer Effizienzscore des modellierten Aufgabenabschlusses "
            "auf einer Skala von 0 bis 100."
        ),
        metric_type="score",
        source="predefined",
        analysis_question="Welche Aussage beantwortet diese Metrik?",
        data_basis="Reading Speed, Attention und Aufgabenerfolgswert",
        limitation="Vergleichsscore für die Simulation, keine echte Nutzungszeit.",
        expected_output_range=(0, 100),
        higher_is_better=True,
        tags=["completion", "efficiency"],
    ),
    EvaluationMetricDefinition(
        metric_id="task_success_score",
        name="Aufgabenerfolgswert",
        description=(
            "Heuristischer Aufgabenerfolgswert auf einer Skala von 0 bis 100; "
            "keine statistisch kalibrierte Wahrscheinlichkeit."
        ),
        metric_type="score",
        source="predefined",
        analysis_question="Welche Aussage beantwortet diese Metrik?",
        data_basis="Error Risk, Cognitive Load und Navigation Effort",
        limitation="Heuristischer Score, keine statistische Erfolgswahrscheinlichkeit.",
        expected_output_range=(0, 100),
        higher_is_better=True,
        tags=["success", "score"],
    ),
    EvaluationMetricDefinition(
        metric_id="completion_time",
        name="Bearbeitungszeit",
        description=(
            "Tatsächliche Gesamtdauer bis zum Abschluss der Aufgabe in Sekunden."
        ),
        metric_type="time",
        source="predefined",
        analysis_question="Wie lange dauert die vollständige Aufgabenbearbeitung?",
        data_basis="Task Progress, GOMS-Basisdauern und Profilzustände",
        limitation="Simulierte Bearbeitungszeit, keine gemessene Nutzungszeit.",
        expected_output_range=(0, 3600),
        higher_is_better=False,
        tags=["time", "completion"],
    ),
    EvaluationMetricDefinition(
        metric_id="time_limit_risk",
        name="Zeitlimit-Risiko",
        description=(
            "Heuristischer Risikoscore dafür, ein vorgegebenes Zeitlimit "
            "zu überschreiten; keine empirisch kalibrierte Wahrscheinlichkeit."
        ),
        metric_type="score",
        source="predefined",
        analysis_question="Wie kritisch ist das Verhältnis von Bearbeitungszeit und Zeitlimit?",
        data_basis="Completion Time und konfiguriertes Zeitlimit",
        limitation="Heuristischer Risikoscore abhängig vom gewählten Zeitlimit.",
        expected_output_range=(0, 100),
        higher_is_better=False,
        tags=["time", "risk"],
    ),
)

_METRICS_BY_ID = {
    metric.metric_id: metric for metric in _PREDEFINED_EVALUATION_METRICS
}

_RETIRED_METRIC_IDS = {
    "dyslexia_reading_load",
    "adhd_interaction_load",
}

_METRIC_ALIASES = {
    "task_success_probability": "task_success_score",
}


def canonical_metric_id(metric_id: str) -> str:
    return _METRIC_ALIASES.get(metric_id, metric_id)


def get_predefined_evaluation_metrics() -> list[EvaluationMetricDefinition]:
    return [metric.model_copy(deep=True) for metric in _PREDEFINED_EVALUATION_METRICS]


def get_retired_evaluation_metric_ids() -> set[str]:
    return set(_RETIRED_METRIC_IDS)


def get_metric_by_id(metric_id: str) -> EvaluationMetricDefinition | None:
    metric = _METRICS_BY_ID.get(canonical_metric_id(metric_id))
    return metric.model_copy(deep=True) if metric is not None else None


def build_default_evaluation_metrics_selection(
    metric_ids: list[str] | None = None,
) -> EvaluationMetricsSelection:
    selected_ids = metric_ids or [
        metric.metric_id for metric in _PREDEFINED_EVALUATION_METRICS
    ]
    selected_ids = list(
        dict.fromkeys(canonical_metric_id(metric_id) for metric_id in selected_ids)
    )
    selected_ids = [
        metric_id
        for metric_id in selected_ids
        if metric_id not in _RETIRED_METRIC_IDS
    ]
    unknown_ids = [
        metric_id
        for metric_id in selected_ids
        if metric_id not in _METRICS_BY_ID
    ]
    if unknown_ids:
        raise ValueError(
            "Unknown predefined evaluation metric IDs: "
            + ", ".join(unknown_ids)
        )

    return EvaluationMetricsSelection(
        selected_metrics=[
            _METRICS_BY_ID[metric_id].model_copy(deep=True)
            for metric_id in selected_ids
        ]
    )
