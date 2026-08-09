from collections.abc import Sequence

from backend.domains.simulation.schemas.types import UserState
from backend.domains.simulation.values import weighted_sum


class CompletionEfficiencyMetric:
    metric_id = "completion_efficiency"

    def calculate(
        self,
        *,
        user_state: UserState,
        task_success_score: float,
        weights: Sequence[float] | None = None,
    ) -> float:
        return weighted_sum(
            (
                user_state["reading_speed"],
                user_state["attention"],
                task_success_score,
            ),
            weights,
        )
