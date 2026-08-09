from collections.abc import Sequence

from backend.domains.simulation.schemas.types import UserState
from backend.domains.simulation.values import attribute_value, weighted_sum


class ErrorRiskAlgorithm:
    algorithm_id = "metric.error_risk.weighted_sum"

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
        parameters = computed_task_parameters or {}
        base_risk = weighted_sum(
            (
                cognitive_load,
                user_state["fatigue"],
                attribute_value(environment_model, "time_pressure"),
                100 - user_state["attention"],
            ),
            weights,
        )
        return min(
            100.0,
            base_risk
            + parameters.get("dyslexia_reading_load", 0.0)
            * dyslexia_load_effect
            + parameters.get("adhd_interaction_load", 0.0)
            * adhd_load_effect,
        )
