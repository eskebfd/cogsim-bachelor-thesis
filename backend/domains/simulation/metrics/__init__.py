from collections.abc import Sequence

import backend.domains.simulation.algorithms
from backend.domains.simulation.config import (
    DEFAULT_SIMULATION_CONFIG,
    SimulationConfig,
)
from backend.domains.simulation.metrics.cognitive_load import CognitiveLoadMetric
from backend.domains.simulation.metrics.completion_efficiency import (
    CompletionEfficiencyMetric,
)
from backend.domains.simulation.metrics.completion_time import CompletionTimeMetric
from backend.domains.simulation.metrics.error_risk import ErrorRiskMetric
from backend.domains.simulation.metrics.registry import (
    METRIC_REGISTRY,
    calculate_metric,
    register_metric,
)
from backend.domains.simulation.metrics.task_success import TaskSuccessMetric
from backend.domains.simulation.metrics.time_limit_risk import TimeLimitRiskMetric
from backend.domains.simulation.schemas.types import ResultMetrics, UserState


for _metric in (
    CognitiveLoadMetric(),
    ErrorRiskMetric(),
    TaskSuccessMetric(),
    CompletionEfficiencyMetric(),
    CompletionTimeMetric(),
    TimeLimitRiskMetric(),
):
    register_metric(_metric)

METRIC_REGISTRY.register_alias("task_success_probability", "task_success_score")


def calculate_cognitive_load(
    task_model: dict,
    computed_task_parameters: dict[str, float],
    user_state: UserState,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet die modellierte kognitive Belastung anhand eines
    gewichteten linearen Modells.
    """
    return calculate_metric(
        "cognitive_load",
        task_model=task_model,
        computed_task_parameters=computed_task_parameters,
        user_state=user_state,
        weights=weights,
    )


def calculate_error_risk(
    cognitive_load: float,
    user_state: UserState,
    environment_model: dict,
    computed_task_parameters: dict[str, float] | None = None,
    dyslexia_load_effect: float = 0.15,
    adhd_load_effect: float = 0.12,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet das modellierte Fehlerrisiko auf Basis der aktuellen
    Belastung, Aufmerksamkeit und Umgebungsbedingungen.
    """
    return calculate_metric(
        "error_risk",
        cognitive_load=cognitive_load,
        user_state=user_state,
        environment_model=environment_model,
        computed_task_parameters=computed_task_parameters,
        dyslexia_load_effect=dyslexia_load_effect,
        adhd_load_effect=adhd_load_effect,
        weights=weights,
    )


def calculate_task_success_score(
    error_risk: float,
    cognitive_load: float,
    computed_task_parameters: dict[str, float],
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet den heuristischen Aufgabenerfolgswert.

    Hohe Belastung, hohes Fehlerrisiko und hoher Navigationsaufwand
    reduzieren diesen Score.
    """
    return calculate_metric(
        "task_success_score",
        error_risk=error_risk,
        cognitive_load=cognitive_load,
        computed_task_parameters=computed_task_parameters,
        weights=weights,
    )


def calculate_completion_efficiency(
    user_state: UserState,
    task_success_score: float,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet die modellierte Bearbeitungseffizienz auf Grundlage
    des Nutzerzustands und des Aufgabenerfolgswerts.
    """
    return calculate_metric(
        "completion_efficiency",
        user_state=user_state,
        task_success_score=task_success_score,
        weights=weights,
    )


def calculate_result_metrics(
    task_model: dict,
    environment_model: dict,
    computed_task_parameters: dict[str, float],
    user_state: UserState,
    config: SimulationConfig = DEFAULT_SIMULATION_CONFIG,
) -> ResultMetrics:
    """
    Berechnet alle Ergebnismetriken eines Simulationsschritts.

    Die Metriken werden aufeinander aufbauend berechnet und bilden
    den aktuellen Zustand der Simulation ab.
    """
    cognitive_load = calculate_cognitive_load(
        task_model,
        computed_task_parameters,
        user_state,
        config.model_weights.get("cognitive_load"),
    )
    error_risk = calculate_error_risk(
        cognitive_load,
        user_state,
        environment_model,
        computed_task_parameters,
        config.error_risk_dyslexia_load_effect,
        config.error_risk_adhd_load_effect,
        config.model_weights.get("error_risk"),
    )
    task_success_score = calculate_task_success_score(
        error_risk,
        cognitive_load,
        computed_task_parameters,
        config.model_weights.get("task_success_score"),
    )
    completion_efficiency = calculate_completion_efficiency(
        user_state,
        task_success_score,
        config.model_weights.get("completion_efficiency"),
    )
    return {
        "cognitive_load": cognitive_load,
        "error_risk": error_risk,
        "task_success_score": task_success_score,
        "completion_efficiency": completion_efficiency,
    }


__all__ = [
    "METRIC_REGISTRY",
    "calculate_cognitive_load",
    "calculate_completion_efficiency",
    "calculate_error_risk",
    "calculate_result_metrics",
    "calculate_task_success_score",
]
