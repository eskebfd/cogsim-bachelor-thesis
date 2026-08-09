from backend.domains.evaluation.registries.dimensions import (
    get_evaluation_dimension_by_id,
    get_evaluation_dimensions,
)
from backend.domains.evaluation.registries.goals import (
    get_evaluation_goal_by_id,
    get_evaluation_goals,
)
from backend.domains.evaluation.schemas.evaluation_metrics import (
    EvaluationDimensionDefinition,
    EvaluationGoalSelection,
    EvaluationMetricsSelection,
    ResolvedEvaluationSelection,
)
from backend.domains.evaluation.registries.metrics import (
    get_metric_by_id,
)


def _deduplicate(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _resolve_dimensions(
    dimension_ids: list[str],
) -> list[EvaluationDimensionDefinition]:
    dimensions = []
    for dimension_id in _deduplicate(dimension_ids):
        dimension = get_evaluation_dimension_by_id(dimension_id)
        if dimension is None:
            raise ValueError(
                "Evaluation goal registry references unknown dimension ID: "
                f"{dimension_id}"
            )
        dimensions.append(dimension)
    return dimensions


def _metric_ids_from_dimensions(
    dimensions: list[EvaluationDimensionDefinition],
) -> list[str]:
    metric_ids = []
    for dimension in dimensions:
        metric_ids.extend(dimension.metric_ids)
    return _deduplicate(metric_ids)


def _resolve_metrics(metric_ids: list[str]) -> EvaluationMetricsSelection:
    metrics = []
    for metric_id in metric_ids:
        metric = get_metric_by_id(metric_id)
        if metric is None:
            raise ValueError(
                "Evaluation dimension registry references unknown metric ID: "
                f"{metric_id}"
            )
        metrics.append(metric)
    return EvaluationMetricsSelection(selected_metrics=metrics)


def resolve_evaluation_goal_selection(
    selection: EvaluationGoalSelection,
) -> ResolvedEvaluationSelection:
    selected_goals = []
    dimension_ids = []

    for goal_id in _deduplicate(selection.selected_goal_ids):
        goal = get_evaluation_goal_by_id(goal_id)
        if goal is None:
            raise ValueError(f"Unknown evaluation goal ID: {goal_id}")
        selected_goals.append(goal)
        dimension_ids.extend(goal.dimension_ids)

    dimensions = _resolve_dimensions(dimension_ids)
    metric_ids = _metric_ids_from_dimensions(dimensions)

    notes = []
    if not metric_ids and selection.custom_metric_requests:
        notes.append(
            "Custom metric requests are preserved as notes, but cannot create "
            "simulation metrics without a registry mapping."
        )

    if not metric_ids:
        raise ValueError(
            "Evaluation goal selection does not resolve to any known metrics. "
            "Select at least one predefined evaluation goal."
        )

    selected_metrics = _resolve_metrics(metric_ids)
    selected_metrics.custom_metric_requests = list(
        selection.custom_metric_requests
    )

    return ResolvedEvaluationSelection(
        selected_goals=selected_goals,
        resolved_dimensions=dimensions,
        selected_metrics=selected_metrics,
        custom_metric_requests=list(selection.custom_metric_requests),
        notes=notes,
    )


def validate_evaluation_registry() -> None:
    for goal in get_evaluation_goals():
        _resolve_dimensions(goal.dimension_ids)

    for dimension in get_evaluation_dimensions():
        _resolve_metrics(dimension.metric_ids)
