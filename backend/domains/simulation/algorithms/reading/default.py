from collections.abc import Sequence

from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.values import (
    attribute_value,
    clamp,
    rounded,
    validated_weights,
)


class ReadingSpeedAlgorithm:
    algorithm_id = "reading.base_speed"

    def calculate(
        self,
        *,
        user_model: dict,
        interface_model: dict,
        environment_model: dict,
        computed_task_parameters: dict[str, float],
        dyslexia_load_effect: float = 0.20,
        weights: Sequence[float] | None = None,
    ) -> float:
        w1, w2, w3, w4 = validated_weights(weights, 4)
        dyslexia_processing_vulnerability = (
            (100.0 - attribute_value(user_model, "sublexical_decoding_stability", 75.0))
            + (
                100.0
                - attribute_value(
                    user_model,
                    "orthographic_processing_stability",
                    75.0,
                )
            )
            + (
                100.0
                - attribute_value(
                    user_model,
                    "parallel_letter_processing_stability",
                    75.0,
                )
            )
        ) / 3
        dyslexia_load_penalty = (
            computed_task_parameters.get("dyslexia_reading_load", 0.0)
            * dyslexia_processing_vulnerability
            / 100.0
        )
        value = (
            100
            - w1 * attribute_value(user_model, "reading_difficulty")
            - w2 * computed_task_parameters["text_complexity"]
            - w3 * attribute_value(environment_model, "noise_level")
            + w4 * attribute_value(interface_model, "accessibility_support")
            - dyslexia_load_effect * dyslexia_load_penalty
        )
        return rounded(value)


class ReadingSpeedUpdateAlgorithm:
    algorithm_id = "reading.update"

    def calculate(
        self,
        *,
        user_model: dict,
        interface_model: dict,
        environment_model: dict,
        computed_task_parameters: dict[str, float],
        config: SimulationConfig,
        attention: float,
        fatigue: float,
        modifier: float = 1.0,
    ) -> float:
        from backend.domains.simulation.algorithms.registry import calculate_with_algorithm

        base_speed = calculate_with_algorithm(
            "reading.base_speed",
            user_model=user_model,
            interface_model=interface_model,
            environment_model=environment_model,
            computed_task_parameters=computed_task_parameters,
            dyslexia_load_effect=config.reading_dyslexia_load_effect,
            weights=config.model_weights.get("reading_speed"),
        )
        state_factor = clamp(
            1
            - config.reading_fatigue_effect * (fatigue / 100)
            - config.reading_attention_effect * ((100 - attention) / 100),
            config.minimum_reading_speed_factor,
            1.0,
        )
        return rounded(base_speed * state_factor * modifier)
