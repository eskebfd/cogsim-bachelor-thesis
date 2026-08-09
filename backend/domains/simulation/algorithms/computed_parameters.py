from collections.abc import Sequence

from backend.domains.simulation.values import (
    attribute_value,
    parameter_value,
    rounded,
    weighted_sum,
)


def calculate_text_complexity(
    interface_model: dict,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet die Textkomplexität aus den textbezogenen
    Interface-Attributen mithilfe eines gewichteten linearen Modells.
    """
    return weighted_sum(
        (
            attribute_value(interface_model, "sentence_length"),
            attribute_value(interface_model, "word_difficulty"),
            attribute_value(interface_model, "technical_terms"),
            attribute_value(interface_model, "text_volume"),
        ),
        weights,
    )


def calculate_navigation_effort(
    task_model: dict,
    interface_model: dict,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet den Navigationsaufwand auf Basis von
    Interface- und Aufgabenattributen.
    """
    return weighted_sum(
        (
            attribute_value(interface_model, "navigation_complexity"),
            attribute_value(interface_model, "visual_clutter"),
            attribute_value(task_model, "number_of_steps"),
        ),
        weights,
    )


def calculate_decoding_load(
    task_model: dict,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet den dyslexierelevanten Dekodieraufwand aus
    Leseanforderung, unbekannten Wörtern, orthografischem Anspruch
    und morphologischer Komplexität.
    """
    return weighted_sum(
        (
            attribute_value(task_model, "reading_demand"),
            attribute_value(task_model, "unfamiliar_word_density", 20.0),
            attribute_value(task_model, "orthographic_irregularity", 20.0),
            attribute_value(task_model, "morphological_complexity", 25.0),
        ),
        weights,
    )


def calculate_visual_reading_load(
    interface_model: dict,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Berechnet die visuelle Lesebelastung aus Textdichte,
    Zeilenverfolgung, visueller Unruhe und inverser Lesbarkeit.
    """
    return weighted_sum(
        (
            attribute_value(interface_model, "text_density", 35.0),
            attribute_value(interface_model, "line_tracking_difficulty", 25.0),
            attribute_value(interface_model, "visual_clutter"),
            100.0 - attribute_value(interface_model, "text_legibility", 75.0),
        ),
        weights,
    )


def calculate_dyslexia_reading_load(
    task_model: dict,
    interface_model: dict,
    text_complexity: float,
    decoding_load: float,
    visual_reading_load: float,
    weights: Sequence[float] | None = None,
) -> float:
    """
    Fasst dyslexierelevante Lese- und Interfacebelastung zu einem
    gemeinsamen Einflussfaktor zusammen.
    """
    return weighted_sum(
        (
            decoding_load,
            visual_reading_load,
            attribute_value(task_model, "reading_demand"),
            text_complexity,
        ),
        weights,
    )


def calculate_sustained_attention_load(
    task_model: dict,
    environment_model: dict,
    weights: Sequence[float] | None = None,
) -> float:
    return weighted_sum(
        (
            attribute_value(task_model, "sustained_attention_demand", 35.0),
            attribute_value(environment_model, "time_pressure", 0.0),
            attribute_value(task_model, "task_complexity"),
            attribute_value(environment_model, "distractions", 0.0),
        ),
        weights,
    )


def calculate_inhibition_load(
    task_model: dict,
    interface_model: dict,
    weights: Sequence[float] | None = None,
) -> float:
    return weighted_sum(
        (
            attribute_value(task_model, "inhibition_demand", 25.0),
            attribute_value(interface_model, "irrelevant_signal_load", 25.0),
            attribute_value(interface_model, "visual_clutter"),
            attribute_value(interface_model, "feedback_interruptiveness", 25.0),
        ),
        weights,
    )


def calculate_attention_switching_load(
    task_model: dict,
    interface_model: dict,
    weights: Sequence[float] | None = None,
) -> float:
    return weighted_sum(
        (
            attribute_value(task_model, "task_switching_demand", 30.0),
            attribute_value(interface_model, "navigation_complexity"),
            attribute_value(task_model, "memory_demand"),
            attribute_value(task_model, "divided_attention_demand", 30.0),
        ),
        weights,
    )


def calculate_adhd_interaction_load(
    interface_model: dict,
    sustained_attention_load: float,
    inhibition_load: float,
    attention_switching_load: float,
    weights: Sequence[float] | None = None,
) -> float:
    return weighted_sum(
        (
            sustained_attention_load,
            inhibition_load,
            attention_switching_load,
            attribute_value(interface_model, "visual_clutter"),
        ),
        weights,
    )


def resolve_computed_task_parameters(
    task_model: dict,
    interface_model: dict,
    computed_task_parameters: dict,
    environment_model: dict | None = None,
    model_weights: dict[str, tuple[float, ...]] | None = None,
) -> dict[str, float]:
    """
    Ermittelt alle berechneten Aufgabenparameter.

    Bereits vorhandene Werte aus dem Simulation Model werden übernommen.
    Fehlt ein Parameter, wird er deterministisch aus den Basisattributen
    berechnet.
    """

    configured_weights = model_weights or {}
    environment = environment_model or {}


    text_complexity = parameter_value(
        computed_task_parameters,
        "text_complexity",
        calculate_text_complexity(
            interface_model,
            configured_weights.get("text_complexity"),
        ),
    )


    navigation_effort = parameter_value(
        computed_task_parameters,
        "navigation_effort",
        calculate_navigation_effort(
            task_model,
            interface_model,
            configured_weights.get("navigation_effort"),
        ),
    )
    decoding_load = parameter_value(
        computed_task_parameters,
        "decoding_load",
        calculate_decoding_load(
            task_model,
            configured_weights.get("decoding_load"),
        ),
    )
    visual_reading_load = parameter_value(
        computed_task_parameters,
        "visual_reading_load",
        calculate_visual_reading_load(
            interface_model,
            configured_weights.get("visual_reading_load"),
        ),
    )
    dyslexia_reading_load = parameter_value(
        computed_task_parameters,
        "dyslexia_reading_load",
        calculate_dyslexia_reading_load(
            task_model,
            interface_model,
            text_complexity,
            decoding_load,
            visual_reading_load,
            configured_weights.get("dyslexia_reading_load"),
        ),
    )
    sustained_attention_load = parameter_value(
        computed_task_parameters,
        "sustained_attention_load",
        calculate_sustained_attention_load(
            task_model,
            environment,
            configured_weights.get("sustained_attention_load"),
        ),
    )
    inhibition_load = parameter_value(
        computed_task_parameters,
        "inhibition_load",
        calculate_inhibition_load(
            task_model,
            interface_model,
            configured_weights.get("inhibition_load"),
        ),
    )
    attention_switching_load = parameter_value(
        computed_task_parameters,
        "attention_switching_load",
        calculate_attention_switching_load(
            task_model,
            interface_model,
            configured_weights.get("attention_switching_load"),
        ),
    )
    adhd_interaction_load = parameter_value(
        computed_task_parameters,
        "adhd_interaction_load",
        calculate_adhd_interaction_load(
            interface_model,
            sustained_attention_load,
            inhibition_load,
            attention_switching_load,
            configured_weights.get("adhd_interaction_load"),
        ),
    )


    return {
        "text_complexity": rounded(text_complexity),
        "navigation_effort": rounded(navigation_effort),
        "decoding_load": rounded(decoding_load),
        "visual_reading_load": rounded(visual_reading_load),
        "dyslexia_reading_load": rounded(dyslexia_reading_load),
        "sustained_attention_load": rounded(sustained_attention_load),
        "inhibition_load": rounded(inhibition_load),
        "attention_switching_load": rounded(attention_switching_load),
        "adhd_interaction_load": rounded(adhd_interaction_load),
    }
