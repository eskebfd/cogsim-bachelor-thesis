from backend.domains.simulation.values import attribute_value


def build_input_factors(
    user_model: dict,
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    computed_task_parameters: dict[str, float],
) -> dict:
    """
    Erstellt alle Eingangsgrößen der Simulation.

    Die Faktoren werden aus den Basisattributen der Modelle sowie den
    berechneten Aufgabenparametern zusammengeführt und dienen als
    Eingabe für die Zustands- und Metrikberechnung.
    """
    return {

        "user_profile": user_model.get("user_type", "generic"),
        "reading_difficulty": attribute_value(
            user_model,
            "reading_difficulty",
        ),
        "attention_stability": attribute_value(
            user_model,
            "attention_stability",
        ),
        "distraction_sensitivity": attribute_value(
            user_model,
            "distraction_sensitivity",
        ),

        "text_complexity": computed_task_parameters["text_complexity"],
        "navigation_effort": computed_task_parameters["navigation_effort"],

        "noise_level": attribute_value(environment_model, "noise_level"),
        "context_stability": attribute_value(
            environment_model,
            "context_stability",
        ),
        "distractions": attribute_value(environment_model, "distractions"),
        "time_pressure": attribute_value(environment_model, "time_pressure"),

        "accessibility_support": attribute_value(
            interface_model,
            "accessibility_support",
        ),

        "task_complexity": attribute_value(task_model, "task_complexity"),
        "reading_demand": attribute_value(task_model, "reading_demand"),
        "input_demand": attribute_value(task_model, "input_demand"),
        "memory_demand": attribute_value(task_model, "memory_demand"),
    }
