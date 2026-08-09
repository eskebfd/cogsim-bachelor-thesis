from collections.abc import Sequence

import backend.domains.simulation.algorithms
from backend.domains.simulation.algorithms.registry import calculate_with_algorithm
from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import UserState
from backend.domains.simulation.values import (
    attribute_value,
    rounded,
)


def calculate_reading_speed(
    user_model: dict,
    interface_model: dict,
    environment_model: dict,
    computed_task_parameters: dict[str, float],
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet die modellierte Lesegeschwindigkeit.

    Leseschwierigkeit, Textkomplexität und Lärm reduzieren die
    Geschwindigkeit, unterstützende Interface-Funktionen erhöhen sie.
    """
    return calculate_with_algorithm(
        "reading.base_speed",
        user_model=user_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=computed_task_parameters,
        weights=weights,
    )


def calculate_attention_decay(
    user_model: dict,
    interface_model: dict,
    environment_model: dict,
    fatigue: float,
    config: SimulationConfig,
    computed_task_parameters: dict[str, float] | None = None,
) -> float:
    """
    Berechnet den Aufmerksamkeitsverlust pro Sekunde.

    Risikofaktoren erhöhen den Verlust, unterstützende Faktoren
    reduzieren ihn.
    """
    return calculate_with_algorithm(
        "attention.linear_decay",
        user_model=user_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=computed_task_parameters,
        fatigue=fatigue,
        config=config,
    )


def calculate_fatigue_target(
    task_model: dict,
    environment_model: dict,
    attention: float,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet den Zielwert der mentalen Ermüdung.

    Hohe Aufgabenanforderungen, Zeitdruck und niedrige Aufmerksamkeit
    erhöhen den Ermüdungszielwert.
    """
    return calculate_with_algorithm(
        "fatigue.target",
        task_model=task_model,
        environment_model=environment_model,
        attention=attention,
        weights=weights,
    )


def linear_transition(
    current_value: float,
    target_value: float,
    response_rate: float,
    time_step_seconds: int,
) -> float:
    """
    Bewegt einen aktuellen Zustandswert linear in Richtung Zielwert.

    Die response_rate bestimmt, wie stark sich der Zustand pro
    Simulationsschritt an den Zielwert annähert.
    """
    return calculate_with_algorithm(
        "fatigue.linear_transition",
        current_value=current_value,
        target_value=target_value,
        response_rate=response_rate,
        time_step_seconds=time_step_seconds,
    )


def initialize_user_state(
    user_model: dict,
    config: SimulationConfig,
) -> UserState:
    """
    Initialisiert den User State zu Beginn der Simulation.
    """
    return {
        "reading_speed": 0.0,
        "attention": rounded(
            config.initial_attention
            if config.initial_attention is not None
            else attribute_value(user_model, "attention_stability", 50.0)
        ),
        "fatigue": rounded(config.initial_fatigue),
    }


def update_reading_speed(
    user_model: dict,
    interface_model: dict,
    environment_model: dict,
    computed_task_parameters: dict[str, float],
    config: SimulationConfig,
    attention: float,
    fatigue: float,
    modifier: float = 1.0,
) -> float:
    """
    Aktualisiert die Lesegeschwindigkeit für den aktuellen Simulationsschritt.
    """
    return calculate_with_algorithm(
        "reading.update",
        user_model=user_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=computed_task_parameters,
        config=config,
        attention=attention,
        fatigue=fatigue,
        modifier=modifier,
    )


def update_attention(
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
    """
    Aktualisiert die Aufmerksamkeit über den zeitlichen Verlauf.
    """
    return calculate_with_algorithm(
        "attention.update",
        current_attention=current_attention,
        user_model=user_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=computed_task_parameters,
        fatigue=fatigue,
        config=config,
        time_step_seconds=time_step_seconds,
        modifier=modifier,
    )


def update_fatigue(
    current_fatigue: float,
    task_model: dict,
    environment_model: dict,
    attention: float,
    config: SimulationConfig,
    time_step_seconds: float,
    modifier: float = 1.0,
) -> float:
    """
    Aktualisiert die mentale Ermüdung über eine lineare Annäherung
    an den berechneten Zielwert.
    """
    return calculate_with_algorithm(
        "fatigue.update",
        current_fatigue=current_fatigue,
        task_model=task_model,
        environment_model=environment_model,
        attention=attention,
        config=config,
        time_step_seconds=time_step_seconds,
        modifier=modifier,
    )


def update_user_state(
    current_state: UserState,
    user_model: dict,
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    computed_task_parameters: dict[str, float],
    config: SimulationConfig,
    time_step_seconds: float | None = None,
    step_modifier: dict[str, float | str] | None = None,
) -> UserState:
    """
    Aktualisiert den gesamten User State für einen Simulationsschritt.

    Dabei werden Reading Speed, Attention und Fatigue nacheinander aus
    den aktuellen Modellwerten und optionalen Schritt-Modifikatoren berechnet.
    """
    elapsed_seconds = time_step_seconds or config.time_step_seconds
    modifiers = step_modifier or {}


    attention = update_attention(
        current_state["attention"],
        user_model,
        interface_model,
        environment_model,
        current_state["fatigue"],
        config,
        elapsed_seconds,
        float(modifiers.get("attention_modifier", 1.0)),
        computed_task_parameters,
    )


    fatigue = update_fatigue(
        current_state["fatigue"],
        task_model,
        environment_model,
        attention,
        config,
        elapsed_seconds,
        float(modifiers.get("fatigue_modifier", 1.0)),
    )


    reading_speed = update_reading_speed(
        user_model,
        interface_model,
        environment_model,
        computed_task_parameters,
        config,
        attention,
        fatigue,
        float(modifiers.get("reading_speed_modifier", 1.0)),
    )

    return {
        "reading_speed": reading_speed,
        "attention": attention,
        "fatigue": fatigue,
    }
