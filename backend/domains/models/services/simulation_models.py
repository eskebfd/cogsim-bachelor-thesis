from backend.domains.simulation.schemas.simulation_model import SimulationModelSchema
from backend.domains.models.services.model_attributes import numeric_attribute_value
from backend.domains.simulation.config import DEFAULT_SIMULATION_CONFIG
from backend.domains.simulation.weights import normalize_weights


def build_simulation_model(
    user_model: dict,
) -> SimulationModelSchema:
    config = DEFAULT_SIMULATION_CONFIG
    model_weights = {
        name: normalize_weights(values, len(values))
        for name, values in config.model_weights.items()
    }

    return SimulationModelSchema.model_validate(
        {
            "time_step_seconds": config.time_step_seconds,
            "enable_task_abandonment": config.enable_task_abandonment,
            "max_step_duration_factor": config.max_step_duration_factor,
            "initial_user_state": {
                "attention": numeric_attribute_value(
                    user_model,
                    "attention_stability",
                    default=50,
                ),
                "fatigue": config.initial_fatigue,
            },
            "response_rates": config.state_response_rates,
            "event_thresholds": config.event_thresholds,
            "model_weights": model_weights,
            "task_step_modifiers": [],
            "assumptions": [
                "Gewichte und Simulationsparameter stammen aus der deterministischen Backend-Konfiguration.",
                "Szenariospezifische Kalibrierung kann später über geprüfte Konfigurationswerte ergänzt werden.",
            ],
        }
    )
