from backend.domains.planning.schemas.computed_parameters import ComputedParametersSchema
from backend.domains.planning.schemas.simulation_plan import SimulationPlanSchema
from backend.domains.models.services.model_attributes import numeric_attribute_value


def _rounded_weighted_mean(values: list[float]) -> int:
    return round(sum(values) / len(values))


def _weights_for_output(
    simulation_plan: SimulationPlanSchema | None,
    output: str,
    attributes: list[str],
) -> dict[str, float]:
    if simulation_plan is not None:
        for model in simulation_plan.computation_models:
            if model.output == output and model.weights:
                if all(attribute in model.weights for attribute in attributes):
                    return {
                        attribute: model.weights[attribute]
                        for attribute in attributes
                    }
    equal_weight = 1 / len(attributes)
    return {attribute: equal_weight for attribute in attributes}


def _weighted_value(values: dict[str, float], weights: dict[str, float]) -> int:
    weight_sum = sum(weights.values())
    if weight_sum <= 0:
        return _rounded_weighted_mean(list(values.values()))
    return round(
        sum(values[attribute] * weights[attribute] for attribute in values)
        / weight_sum
    )


def build_computed_task_parameters(
    task_model: dict,
    interface_model: dict,
    simulation_plan: SimulationPlanSchema | None = None,
) -> ComputedParametersSchema:
    text_attributes = [
        "text_volume",
        "sentence_length",
        "word_difficulty",
        "technical_terms",
    ]
    navigation_sources = [
        (task_model, "number_of_steps"),
        (interface_model, "visual_clutter"),
        (interface_model, "navigation_complexity"),
    ]
    text_values = [
        numeric_attribute_value(interface_model, attribute)
        for attribute in text_attributes
    ]
    navigation_values = [
        numeric_attribute_value(model, attribute)
        for model, attribute in navigation_sources
    ]
    text_values_by_attribute = dict(zip(text_attributes, text_values))
    navigation_attributes = [attribute for _, attribute in navigation_sources]
    navigation_values_by_attribute = dict(
        zip(navigation_attributes, navigation_values)
    )
    text_weights = _weights_for_output(
        simulation_plan,
        "text_complexity",
        text_attributes,
    )
    navigation_weights = _weights_for_output(
        simulation_plan,
        "navigation_effort",
        navigation_attributes,
    )
    decoding_attributes = [
        "reading_demand",
        "unfamiliar_word_density",
        "orthographic_irregularity",
        "morphological_complexity",
    ]
    decoding_values_by_attribute = {
        attribute: numeric_attribute_value(
            task_model,
            attribute,
            default={
                "reading_demand": 0,
                "unfamiliar_word_density": 20,
                "orthographic_irregularity": 20,
                "morphological_complexity": 25,
            }[attribute],
        )
        for attribute in decoding_attributes
    }
    decoding_weights = _weights_for_output(
        simulation_plan,
        "decoding_load",
        decoding_attributes,
    )
    visual_reading_attributes = [
        "text_density",
        "line_tracking_difficulty",
        "visual_clutter",
        "inverse_text_legibility",
    ]
    visual_reading_values_by_attribute = {
        "text_density": numeric_attribute_value(
            interface_model, "text_density", default=35
        ),
        "line_tracking_difficulty": numeric_attribute_value(
            interface_model, "line_tracking_difficulty", default=25
        ),
        "visual_clutter": numeric_attribute_value(
            interface_model, "visual_clutter"
        ),
        "inverse_text_legibility": 100
        - numeric_attribute_value(interface_model, "text_legibility", default=75),
    }
    visual_reading_weights = _weights_for_output(
        simulation_plan,
        "visual_reading_load",
        visual_reading_attributes,
    )
    decoding_load = _weighted_value(
        decoding_values_by_attribute,
        decoding_weights,
    )
    visual_reading_load = _weighted_value(
        visual_reading_values_by_attribute,
        visual_reading_weights,
    )
    dyslexia_reading_attributes = [
        "decoding_load",
        "visual_reading_load",
        "reading_demand",
        "text_complexity",
    ]
    dyslexia_reading_values_by_attribute = {
        "decoding_load": decoding_load,
        "visual_reading_load": visual_reading_load,
        "reading_demand": numeric_attribute_value(task_model, "reading_demand"),
        "text_complexity": _weighted_value(text_values_by_attribute, text_weights),
    }
    dyslexia_reading_weights = _weights_for_output(
        simulation_plan,
        "dyslexia_reading_load",
        dyslexia_reading_attributes,
    )
    sustained_attention_attributes = [
        "sustained_attention_demand",
        "time_pressure",
        "task_complexity",
        "distractions",
    ]
    sustained_attention_values_by_attribute = {
        "sustained_attention_demand": numeric_attribute_value(
            task_model, "sustained_attention_demand", default=35
        ),
        "time_pressure": numeric_attribute_value(
            interface_model, "time_pressure", default=0
        )
        if "time_pressure" in interface_model
        else 0,
        "task_complexity": numeric_attribute_value(task_model, "task_complexity"),
        "distractions": 0,
    }


    sustained_attention_weights = _weights_for_output(
        simulation_plan,
        "sustained_attention_load",
        sustained_attention_attributes,
    )
    inhibition_attributes = [
        "inhibition_demand",
        "irrelevant_signal_load",
        "visual_clutter",
        "feedback_interruptiveness",
    ]
    inhibition_values_by_attribute = {
        "inhibition_demand": numeric_attribute_value(
            task_model, "inhibition_demand", default=25
        ),
        "irrelevant_signal_load": numeric_attribute_value(
            interface_model, "irrelevant_signal_load", default=25
        ),
        "visual_clutter": numeric_attribute_value(interface_model, "visual_clutter"),
        "feedback_interruptiveness": numeric_attribute_value(
            interface_model, "feedback_interruptiveness", default=25
        ),
    }
    inhibition_weights = _weights_for_output(
        simulation_plan,
        "inhibition_load",
        inhibition_attributes,
    )
    attention_switching_attributes = [
        "task_switching_demand",
        "navigation_complexity",
        "memory_demand",
        "divided_attention_demand",
    ]
    attention_switching_values_by_attribute = {
        "task_switching_demand": numeric_attribute_value(
            task_model, "task_switching_demand", default=30
        ),
        "navigation_complexity": numeric_attribute_value(
            interface_model, "navigation_complexity"
        ),
        "memory_demand": numeric_attribute_value(task_model, "memory_demand"),
        "divided_attention_demand": numeric_attribute_value(
            task_model, "divided_attention_demand", default=30
        ),
    }
    attention_switching_weights = _weights_for_output(
        simulation_plan,
        "attention_switching_load",
        attention_switching_attributes,
    )
    sustained_attention_load = _weighted_value(
        sustained_attention_values_by_attribute,
        sustained_attention_weights,
    )
    inhibition_load = _weighted_value(
        inhibition_values_by_attribute,
        inhibition_weights,
    )
    attention_switching_load = _weighted_value(
        attention_switching_values_by_attribute,
        attention_switching_weights,
    )
    adhd_interaction_attributes = [
        "sustained_attention_load",
        "inhibition_load",
        "attention_switching_load",
        "visual_clutter",
    ]
    adhd_interaction_values_by_attribute = {
        "sustained_attention_load": sustained_attention_load,
        "inhibition_load": inhibition_load,
        "attention_switching_load": attention_switching_load,
        "visual_clutter": numeric_attribute_value(interface_model, "visual_clutter"),
    }
    adhd_interaction_weights = _weights_for_output(
        simulation_plan,
        "adhd_interaction_load",
        adhd_interaction_attributes,
    )
    adhd_interaction_load = _weighted_value(
        adhd_interaction_values_by_attribute,
        adhd_interaction_weights,
    )

    return ComputedParametersSchema.model_validate(
        {
            "text_complexity": {
                "used_basis_attributes": text_attributes,
                "used_weightings": [
                    {"attribute": attribute, "weight": text_weights[attribute]}
                    for attribute in text_attributes
                ],
                "formula": (
                    "0.25 * text_volume + 0.25 * sentence_length + "
                    "0.25 * word_difficulty + 0.25 * technical_terms"
                ),
                "value": _weighted_value(text_values_by_attribute, text_weights),
                "explanation": (
                    "Der Wert wird deterministisch aus den vier "
                    "textbezogenen Interface-Attributen berechnet."
                ),
            },
            "navigation_effort": {
                "used_basis_attributes": [
                    "number_of_steps",
                    "visual_clutter",
                    "navigation_complexity",
                ],
                "used_weightings": [
                    {
                        "attribute": attribute,
                        "weight": navigation_weights[attribute],
                    }
                    for attribute in navigation_attributes
                ],
                "formula": (
                    "(1 / 3) * number_of_steps + (1 / 3) * visual_clutter "
                    "+ (1 / 3) * navigation_complexity"
                ),
                "value": _weighted_value(
                    navigation_values_by_attribute,
                    navigation_weights,
                ),
                "explanation": (
                    "Der Wert wird deterministisch aus Schrittumfang, "
                    "visueller Dichte und Navigationskomplexität berechnet."
                ),
            },
            "decoding_load": {
                "used_basis_attributes": decoding_attributes,
                "used_weightings": [
                    {
                        "attribute": attribute,
                        "weight": decoding_weights[attribute],
                    }
                    for attribute in decoding_attributes
                ],
                "formula": (
                    "0.25 * reading_demand + 0.25 * unfamiliar_word_density "
                    "+ 0.25 * orthographic_irregularity + 0.25 * morphological_complexity"
                ),
                "value": decoding_load,
                "explanation": (
                    "Der Wert bildet den Dekodieraufwand durch Leseumfang, "
                    "unbekannte Wörter, orthografische Irregularität und "
                    "morphologische Komplexität ab."
                ),
            },
            "visual_reading_load": {
                "used_basis_attributes": visual_reading_attributes,
                "used_weightings": [
                    {
                        "attribute": attribute,
                        "weight": visual_reading_weights[attribute],
                    }
                    for attribute in visual_reading_attributes
                ],
                "formula": (
                    "0.25 * text_density + 0.25 * line_tracking_difficulty "
                    "+ 0.25 * visual_clutter + 0.25 * (100 - text_legibility)"
                ),
                "value": visual_reading_load,
                "explanation": (
                    "Der Wert bildet visuelle Lesebelastung durch Textdichte, "
                    "Zeilenverfolgung, visuelle Unruhe und geringe Lesbarkeit ab."
                ),
            },
            "dyslexia_reading_load": {
                "used_basis_attributes": dyslexia_reading_attributes,
                "used_weightings": [
                    {
                        "attribute": attribute,
                        "weight": dyslexia_reading_weights[attribute],
                    }
                    for attribute in dyslexia_reading_attributes
                ],
                "formula": (
                    "0.35 * decoding_load + 0.25 * visual_reading_load "
                    "+ 0.25 * reading_demand + 0.15 * text_complexity"
                ),
                "value": _weighted_value(
                    dyslexia_reading_values_by_attribute,
                    dyslexia_reading_weights,
                ),
                "explanation": (
                    "Der Wert fasst dyslexierelevante Aufgaben- und "
                    "Interface-Lesebelastung zusammen."
                ),
            },
            "sustained_attention_load": {
                "used_basis_attributes": sustained_attention_attributes,
                "used_weightings": [
                    {
                        "attribute": attribute,
                        "weight": sustained_attention_weights[attribute],
                    }
                    for attribute in sustained_attention_attributes
                ],
                "formula": (
                    "0.35 * sustained_attention_demand + 0.25 * time_pressure "
                    "+ 0.20 * task_complexity + 0.20 * distractions"
                ),
                "value": sustained_attention_load,
                "explanation": (
                    "Der Wert beschreibt die Belastung durch längere "
                    "Daueraufmerksamkeit im Aufgabenverlauf."
                ),
            },
            "inhibition_load": {
                "used_basis_attributes": inhibition_attributes,
                "used_weightings": [
                    {
                        "attribute": attribute,
                        "weight": inhibition_weights[attribute],
                    }
                    for attribute in inhibition_attributes
                ],
                "formula": (
                    "0.35 * inhibition_demand + 0.30 * irrelevant_signal_load "
                    "+ 0.20 * visual_clutter + 0.15 * feedback_interruptiveness"
                ),
                "value": inhibition_load,
                "explanation": (
                    "Der Wert beschreibt, wie stark irrelevante Reize oder "
                    "vorschnelle Handlungen gehemmt werden müssen."
                ),
            },
            "attention_switching_load": {
                "used_basis_attributes": attention_switching_attributes,
                "used_weightings": [
                    {
                        "attribute": attribute,
                        "weight": attention_switching_weights[attribute],
                    }
                    for attribute in attention_switching_attributes
                ],
                "formula": (
                    "0.35 * task_switching_demand + 0.25 * navigation_complexity "
                    "+ 0.20 * memory_demand + 0.20 * divided_attention_demand"
                ),
                "value": attention_switching_load,
                "explanation": (
                    "Der Wert beschreibt die Belastung durch Wechsel zwischen "
                    "Schritten, Kontexten und Informationsquellen."
                ),
            },
            "adhd_interaction_load": {
                "used_basis_attributes": adhd_interaction_attributes,
                "used_weightings": [
                    {
                        "attribute": attribute,
                        "weight": adhd_interaction_weights[attribute],
                    }
                    for attribute in adhd_interaction_attributes
                ],
                "formula": (
                    "0.30 * sustained_attention_load + 0.25 * inhibition_load "
                    "+ 0.25 * attention_switching_load + 0.20 * visual_clutter"
                ),
                "value": adhd_interaction_load,
                "explanation": (
                    "Der Wert fasst ADHS-relevante Belastungen durch "
                    "Daueraufmerksamkeit, Inhibition, Wechsel und Reizdichte zusammen."
                ),
            },
            "assumptions": [
                "Alle Eingangswerte werden auf die Skala 0 bis 100 begrenzt.",
                "Solange keine kalibrierten Gewichte vorliegen, werden gleiche Gewichte verwendet.",
            ],
        }
    )
