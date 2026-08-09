from dataclasses import replace

from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.values import clamp


MODEL_WEIGHT_ALIASES = {
    "task_success_probability": "task_success_score",
}


def _number(
    value: object,
    fallback: float,
    minimum: float,
    maximum: float,
) -> float:
    """
    Wandelt einen beliebigen Wert in eine gültige Zahl innerhalb eines
    definierten Wertebereichs um.
    """
    try:
        return clamp(float(value), minimum, maximum)
    except (TypeError, ValueError):
        return fallback


def _boolean(value: object, fallback: bool) -> bool:
    return value if isinstance(value, bool) else fallback


def _weights(
    simulation_model: dict,
    defaults: SimulationConfig,
) -> dict[str, tuple[float, ...]]:
    """
    Übernimmt optionale Modellgewichte aus dem SimulationModel und
    normalisiert sie auf eine Summe von 1.
    """

    configured = dict(simulation_model.get("model_weights", {}) or {})
    for legacy_name, canonical_name in MODEL_WEIGHT_ALIASES.items():
        if canonical_name not in configured and legacy_name in configured:
            configured[canonical_name] = configured[legacy_name]
    merged = dict(defaults.model_weights)

    for name, default_values in defaults.model_weights.items():
        values = configured.get(name)


        if not isinstance(values, list) or len(values) != len(default_values):
            continue


        parsed = tuple(
            _number(value, fallback, 0.0, 1.0)
            for value, fallback in zip(values, default_values)
        )


        total = sum(parsed)
        if total > 0:
            merged[name] = tuple(value / total for value in parsed)

    return merged


def _step_modifiers(simulation_model: dict) -> dict[str, dict[str, float | str]]:
    """
    Liest optionale Modifikatoren einzelner Aufgaben-Schritte aus dem
    SimulationModel ein.
    """

    modifiers = {}

    for item in simulation_model.get("task_step_modifiers", []):
        if not isinstance(item, dict) or not item.get("step_id"):
            continue

        modifiers[str(item["step_id"])] = {
            "attention_modifier": _number(
                item.get("attention_modifier"),
                1.0,
                0.0,
                2.0,
            ),
            "fatigue_modifier": _number(
                item.get("fatigue_modifier"),
                1.0,
                0.0,
                2.0,
            ),
            "reading_speed_modifier": _number(
                item.get("reading_speed_modifier"),
                1.0,
                0.0,
                2.0,
            ),
            "reason": str(item.get("reason", "")),
        }

    return modifiers


def config_from_simulation_model(
    simulation_model: dict | None,
    defaults: SimulationConfig,
) -> SimulationConfig:
    """
    Erstellt aus einem optionalen SimulationModel eine vollständige
    SimulationConfig. Nicht gesetzte Werte werden aus der
    Standardkonfiguration übernommen.
    """


    if not simulation_model:
        return defaults

    initial_state = simulation_model.get("initial_user_state", {})
    response_rates = simulation_model.get("response_rates", {})
    event_thresholds = simulation_model.get("event_thresholds", {})


    return replace(
        defaults,
        time_step_seconds=int(
            _number(
                simulation_model.get("time_step_seconds"),
                defaults.time_step_seconds,
                1,
                10,
            )
        ),
        enable_task_abandonment=_boolean(
            simulation_model.get("enable_task_abandonment"),
            defaults.enable_task_abandonment,
        ),
        max_step_duration_factor=_number(
            simulation_model.get("max_step_duration_factor"),
            defaults.max_step_duration_factor,
            1.0,
            100.0,
        ),

        initial_attention=_number(
            initial_state.get("attention"),
            defaults.initial_attention or 50.0,
            0.0,
            100.0,
        ),
        initial_fatigue=_number(
            initial_state.get("fatigue"),
            defaults.initial_fatigue,
            0.0,
            100.0,
        ),

        state_response_rates={
            "attention": _number(
                response_rates.get("attention"),
                defaults.state_response_rates.get("attention", 1.0),
                0.0,
                1.0,
            ),
            "fatigue": _number(
                response_rates.get("fatigue"),
                defaults.state_response_rates.get("fatigue", 0.05),
                0.0,
                1.0,
            ),
        },

        event_thresholds={
            name: _number(
                event_thresholds.get(name),
                fallback,
                0.0,
                100.0,
            )
            for name, fallback in defaults.event_thresholds.items()
        },

        model_weights=_weights(simulation_model, defaults),

        task_step_modifiers=_step_modifiers(simulation_model),
    )
