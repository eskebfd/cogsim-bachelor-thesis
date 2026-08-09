from collections.abc import Sequence

from backend.domains.simulation.schemas.types import UserState
from backend.domains.simulation.values import attribute_value, weighted_sum


class CognitiveLoadAlgorithm:
    algorithm_id = "metric.cognitive_load.weighted_sum"

    def calculate(
        self,
        *,
        task_model: dict,
        computed_task_parameters: dict[str, float],
        user_state: UserState,
        weights: Sequence[float] | None = None,
    ) -> float:
        return weighted_sum(
            (
                attribute_value(task_model, "task_complexity"),
                computed_task_parameters["text_complexity"],
                attribute_value(task_model, "memory_demand"),
                computed_task_parameters["navigation_effort"],
                user_state["fatigue"],
            ),
            weights,
        )
