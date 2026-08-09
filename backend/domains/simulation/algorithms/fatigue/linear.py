from collections.abc import Sequence

from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.values import (
    attribute_value,
    clamp,
    rounded,
    weighted_sum,
)


class FatigueTargetAlgorithm:
    algorithm_id = "fatigue.target"

    def calculate(
        self,
        *,
        task_model: dict,
        environment_model: dict,
        attention: float,
        weights: Sequence[float] | None = None,
    ) -> float:
        return weighted_sum(
            (
                attribute_value(task_model, "task_complexity"),
                attribute_value(environment_model, "time_pressure"),
                attribute_value(task_model, "reading_demand"),
                attribute_value(task_model, "input_demand"),
                100 - attention,
            ),
            weights,
        )


class LinearTransitionAlgorithm:
    algorithm_id = "fatigue.linear_transition"

    def calculate(
        self,
        *,
        current_value: float,
        target_value: float,
        response_rate: float,
        time_step_seconds: int,
    ) -> float:
        effective_rate = clamp(response_rate * time_step_seconds, 0.0, 1.0)
        return rounded(current_value + effective_rate * (target_value - current_value))


class FatigueUpdateAlgorithm:
    algorithm_id = "fatigue.update"

    def calculate(
        self,
        *,
        current_fatigue: float,
        task_model: dict,
        environment_model: dict,
        attention: float,
        config: SimulationConfig,
        time_step_seconds: float,
        modifier: float = 1.0,
    ) -> float:
        from backend.domains.simulation.algorithms.registry import calculate_with_algorithm

        target = calculate_with_algorithm(
            "fatigue.target",
            task_model=task_model,
            environment_model=environment_model,
            attention=attention,
            weights=config.model_weights.get("fatigue"),
        )
        return calculate_with_algorithm(
            "fatigue.linear_transition",
            current_value=current_fatigue,
            target_value=target,
            response_rate=config.state_response_rates["fatigue"] * modifier,
            time_step_seconds=time_step_seconds,
        )
