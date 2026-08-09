from backend.domains.evaluation.schemas.evaluation_metrics import (
    EvaluationDimensionDefinition,
)


_EVALUATION_DIMENSIONS = (
    EvaluationDimensionDefinition(
        dimension_id="processing_time",
        name="Bearbeitungszeit",
        description="Betrachtet die benötigte Zeit für die vollständige Bearbeitung.",
        criterion=(
            "Die Aufgabe soll ohne unverhältnismäßige Verzögerungen "
            "abgeschlossen werden können."
        ),
        metric_ids=["completion_time"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="completion_efficiency",
        name="Bearbeitungseffizienz",
        description="Betrachtet das Verhältnis zwischen erfolgreichem Fortschritt und Belastung.",
        criterion=(
            "Eine günstige Ausprägung liegt vor, wenn die Aufgabe mit hoher "
            "Effizienz und stabilem Aufgabenerfolgswert bearbeitet wird."
        ),
        metric_ids=["completion_efficiency"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="time_limit_exceedance",
        name="Risiko einer Zeitüberschreitung",
        description="Betrachtet, ob die Bearbeitungsdauer ein Zeitlimit überschreiten kann.",
        criterion=(
            "Problematisch ist ein hoher heuristischer Risikoscore für eine "
            "Überschreitung des verfügbaren Zeitlimits."
        ),
        metric_ids=["time_limit_risk"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="task_success_score",
        name="Aufgabenerfolgswert",
        description=(
            "Betrachtet den heuristischen Score für einen erfolgreichen "
            "Aufgabenabschluss."
        ),
        criterion=(
            "Eine günstige Ausprägung liegt bei hohem Task Success Score vor."
        ),
        metric_ids=["task_success_score"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="error_risk",
        name="Fehlerrisiko",
        description=(
            "Betrachtet den heuristischen Risikoscore fehlerhafter "
            "Interaktionen während der Aufgabe."
        ),
        criterion="Problematisch ist ein erhöhter modellierter Error Risk Score.",
        metric_ids=["error_risk"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="cognitive_load",
        name="Kognitive Belastung",
        description="Betrachtet die modellierte kognitive Beanspruchung des Nutzerprofils.",
        criterion="Problematisch ist eine hohe modellierte Cognitive Load.",
        metric_ids=["cognitive_load"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="load_related_error_risk",
        name="Belastungsbedingtes Fehlerrisiko",
        description=(
            "Betrachtet Fehlerrisiken, die im Zusammenhang mit kognitiver "
            "Beanspruchung und Ermüdung entstehen können."
        ),
        criterion=(
            "Problematisch ist ein erhöhtes Error Risk bei gleichzeitig hoher "
            "kognitiver Belastung."
        ),
        metric_ids=["error_risk"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="profile_time_differences",
        name="Unterschiede im Zeitaufwand",
        description="Betrachtet Unterschiede der Completion Time zwischen Nutzerprofilen.",
        criterion=(
            "Problematisch sind deutliche Unterschiede der Bearbeitungsdauer "
            "zwischen Profilen."
        ),
        metric_ids=["completion_time", "completion_efficiency"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="profile_success_differences",
        name="Unterschiede im Aufgabenerfolgswert",
        description=(
            "Betrachtet Unterschiede des Task Success Score zwischen "
            "Nutzerprofilen."
        ),
        criterion=(
            "Problematisch sind deutlich niedrigere Aufgabenerfolgswerte "
            "für einzelne Profile."
        ),
        metric_ids=["task_success_score"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="profile_cognitive_load_differences",
        name="Unterschiede in der kognitiven Belastung",
        description="Betrachtet Unterschiede der Cognitive Load zwischen Nutzerprofilen.",
        criterion=(
            "Problematisch sind deutlich höhere Belastungswerte für einzelne Profile."
        ),
        metric_ids=["cognitive_load"],
    ),
    EvaluationDimensionDefinition(
        dimension_id="profile_error_risk_differences",
        name="Unterschiede im Fehlerrisiko",
        description="Betrachtet Unterschiede des Error Risk Score zwischen Nutzerprofilen.",
        criterion=(
            "Problematisch sind deutlich erhöhte Fehlerrisiken für einzelne Profile."
        ),
        metric_ids=["error_risk"],
    ),
)

_DIMENSIONS_BY_ID = {
    dimension.dimension_id: dimension for dimension in _EVALUATION_DIMENSIONS
}


def get_evaluation_dimensions() -> list[EvaluationDimensionDefinition]:
    return [
        dimension.model_copy(deep=True)
        for dimension in _EVALUATION_DIMENSIONS
    ]


def get_evaluation_dimension_by_id(
    dimension_id: str,
) -> EvaluationDimensionDefinition | None:
    dimension = _DIMENSIONS_BY_ID.get(dimension_id)
    return dimension.model_copy(deep=True) if dimension is not None else None
