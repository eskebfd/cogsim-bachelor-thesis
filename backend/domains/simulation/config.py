from dataclasses import dataclass, field


def default_model_weights() -> dict[str, tuple[float, ...]]:
    """
    Standardgewichtungen der linearen Modelle.

    Die Gewichtungen werden verwendet, sofern keine expliziten
    Konfigurationen oder validierten Gewichte vorliegen.
    """
    return {
        "text_complexity": (0.25, 0.25, 0.25, 0.25),
        "navigation_effort": (1 / 3, 1 / 3, 1 / 3),
        "decoding_load": (0.25, 0.25, 0.25, 0.25),
        "visual_reading_load": (0.25, 0.25, 0.25, 0.25),
        "dyslexia_reading_load": (0.35, 0.25, 0.25, 0.15),
        "sustained_attention_load": (0.35, 0.25, 0.20, 0.20),
        "inhibition_load": (0.35, 0.30, 0.20, 0.15),
        "attention_switching_load": (0.35, 0.25, 0.20, 0.20),
        "adhd_interaction_load": (0.30, 0.25, 0.25, 0.20),
        "reading_speed": (0.25, 0.25, 0.25, 0.25),
        "attention": (1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 6),
        "fatigue": (0.2, 0.2, 0.2, 0.2, 0.2),
        "cognitive_load": (0.2, 0.2, 0.2, 0.2, 0.2),
        "error_risk": (0.25, 0.25, 0.25, 0.25),
        "task_success_score": (1 / 3, 1 / 3, 1 / 3),
        "completion_efficiency": (1 / 3, 1 / 3, 1 / 3),
    }


@dataclass(frozen=True)
class SimulationConfig:
    """
    Zentrale Konfiguration der zeitdiskreten Simulation.

    Enthält Standardwerte für Zustandsinitialisierung,
    Dynamikparameter und Modellkonfigurationen.
    """


    time_step_seconds: int = 1


    initial_attention: float | None = None


    initial_fatigue: float = 10.0


    attention_base_decay_per_second: float = 0.05
    attention_risk_effect: float = 0.45
    attention_support_effect: float = 0.35

    reading_fatigue_effect: float = 0.20
    reading_attention_effect: float = 0.15
    reading_dyslexia_load_effect: float = 0.20
    error_risk_dyslexia_load_effect: float = 0.15
    attention_adhd_load_effect: float = 0.20
    error_risk_adhd_load_effect: float = 0.12
    minimum_reading_speed_factor: float = 0.50

    max_duration_seconds: float = 300.0
    rework_duration_ratio: float = 0.20
    maximum_rework_seconds: int = 10


    enable_task_abandonment: bool = True
    max_step_duration_factor: float = 3.0


    state_response_rates: dict[str, float] = field(
        default_factory=lambda: {
            "attention": 1.0,
            "fatigue": 0.05,
        }
    )


    event_thresholds: dict[str, float] = field(
        default_factory=lambda: {
            "high_error_risk": 60.0,
            "very_high_cognitive_load": 65.0,
            "very_low_attention": 65.0,
            "time_pressure_warning": 15.0,
            "rework_error_risk": 62.0,
            "high_inhibition_load": 65.0,
            "task_switching_strain": 65.0,
        }
    )


    model_weights: dict[str, tuple[float, ...]] = field(
        default_factory=default_model_weights
    )


    task_step_modifiers: dict[str, dict[str, float | str]] = field(default_factory=dict)


DEFAULT_SIMULATION_CONFIG = SimulationConfig()
