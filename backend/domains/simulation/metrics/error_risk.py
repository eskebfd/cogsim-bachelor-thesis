from collections.abc import Sequence

from backend.domains.simulation.algorithms.registry import calculate_with_algorithm
from backend.domains.simulation.schemas.types import UserState


class ErrorRiskMetric:
    metric_id = "error_risk"

    def calculate(
        self,
        *,
        cognitive_load: float,
        user_state: UserState,
        environment_model: dict,
        computed_task_parameters: dict[str, float] | None = None,
        dyslexia_load_effect: float = 0.15,
        adhd_load_effect: float = 0.12,
        weights: Sequence[float] | None = None,
    ) -> float:
        return calculate_with_algorithm(
            "metric.error_risk.weighted_sum",
            cognitive_load=cognitive_load,
            user_state=user_state,
            environment_model=environment_model,
            computed_task_parameters=computed_task_parameters,
            dyslexia_load_effect=dyslexia_load_effect,
            adhd_load_effect=adhd_load_effect,
            weights=weights,
        )
