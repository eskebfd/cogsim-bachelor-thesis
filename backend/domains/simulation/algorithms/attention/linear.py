from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.values import (
    attribute_value,
    rounded,
    validated_weights,
    weighted_sum,
)


class AttentionDecayAlgorithm:
    algorithm_id = "attention.linear_decay"

    def calculate(
        self,
        *,
        user_model: dict,
        interface_model: dict,
        environment_model: dict,
        fatigue: float,
        config: SimulationConfig,
        computed_task_parameters: dict[str, float] | None = None,
    ) -> float:
        attention_weights = validated_weights(
            config.model_weights.get("attention"),
            6,
        )
        risk_weights = attention_weights[:4]
        support_weights = attention_weights[4:]
        risk_total = sum(risk_weights)
        support_total = sum(support_weights)
        normalized_risk_weights = (
            tuple(weight / risk_total for weight in risk_weights)
            if risk_total
            else None
        )
        normalized_support_weights = (
            tuple(weight / support_total for weight in support_weights)
            if support_total
            else None
        )
        risk = weighted_sum(
            (
                attribute_value(user_model, "distraction_sensitivity"),
                attribute_value(environment_model, "distractions"),
                attribute_value(environment_model, "time_pressure"),
                fatigue,
            ),
            normalized_risk_weights,
        )
        support = weighted_sum(
            (
                attribute_value(interface_model, "accessibility_support"),
                attribute_value(environment_model, "context_stability"),
            ),
            normalized_support_weights,
        )
        parameters = computed_task_parameters or {}
        adhd_load = parameters.get("adhd_interaction_load", 0.0)
        vigilance_factor = (
            100.0 - attribute_value(user_model, "vigilance_stability", 78.0)
        ) / 100.0
        reaction_variability = attribute_value(
            user_model, "reaction_variability", 20.0
        ) / 100.0
        decay = (
            config.attention_base_decay_per_second
            + config.attention_risk_effect * (risk / 100)
            + config.attention_adhd_load_effect
            * (adhd_load / 100)
            * max(vigilance_factor, reaction_variability)
            - config.attention_support_effect * (support / 100)
        )
        return round(max(0.0, decay), 4)


class AttentionUpdateAlgorithm:
    algorithm_id = "attention.update"

    def calculate(
        self,
        *,
        current_attention: float,
        user_model: dict,
        interface_model: dict,
        environment_model: dict,
        fatigue: float,
        config: SimulationConfig,
        time_step_seconds: float | None = None,
        modifier: float = 1.0,
        computed_task_parameters: dict[str, float] | None = None,
    ) -> float:
        from backend.domains.simulation.algorithms.registry import calculate_with_algorithm

        decay = calculate_with_algorithm(
            "attention.linear_decay",
            user_model=user_model,
            interface_model=interface_model,
            environment_model=environment_model,
            computed_task_parameters=computed_task_parameters,
            fatigue=fatigue,
            config=config,
        )
        return rounded(
            current_attention
            - decay
            * (time_step_seconds or config.time_step_seconds)
            * config.state_response_rates.get("attention", 1.0)
            * modifier
        )
