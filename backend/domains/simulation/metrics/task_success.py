from collections.abc import Sequence

from backend.domains.simulation.values import rounded, validated_weights


class TaskSuccessMetric:
    metric_id = "task_success_score"

    def calculate(
        self,
        *,
        error_risk: float,
        cognitive_load: float,
        computed_task_parameters: dict[str, float],
        weights: Sequence[float] | None = None,
    ) -> float:
        w1, w2, w3 = validated_weights(weights, 3)
        weighted_strain = (
            w1 * error_risk
            + w2 * cognitive_load
            + w3 * computed_task_parameters["navigation_effort"]
        )
        return rounded(
            100 - weighted_strain * 0.55
        )
