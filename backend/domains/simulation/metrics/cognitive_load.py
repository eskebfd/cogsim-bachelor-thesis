from collections.abc import Sequence

from backend.domains.simulation.algorithms.registry import calculate_with_algorithm
from backend.domains.simulation.schemas.types import UserState


class CognitiveLoadMetric:
    metric_id = "cognitive_load"

    def calculate(
        self,
        *,
        task_model: dict,
        computed_task_parameters: dict[str, float],
        user_state: UserState,
        weights: Sequence[float] | None = None,
    ) -> float:
        return calculate_with_algorithm(
            "metric.cognitive_load.weighted_sum",
            task_model=task_model,
            computed_task_parameters=computed_task_parameters,
            user_state=user_state,
            weights=weights,
        )
