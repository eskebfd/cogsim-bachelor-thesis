from collections.abc import Mapping
from copy import deepcopy
from typing import Any, Literal

from backend.domains.planning.schemas.simulation_plan import SimulationPlanSchema
from backend.domains.planning.services.computed_parameters import (
    build_computed_task_parameters,
)


EditableScenarioModelType = Literal["task", "interface", "environment"]


EDITABLE_MODEL_ATTRIBUTES: dict[str, tuple[str, ...]] = {
    "task": (
        "task_complexity",
        "number_of_steps",
        "reading_demand",
        "input_demand",
        "memory_demand",
        "decision_demand",
        "error_criticality",
    ),
    "interface": (
        "text_volume",
        "sentence_length",
        "word_difficulty",
        "technical_terms",
        "visual_clutter",
        "navigation_complexity",
        "accessibility_support",
        "feedback_quality",
    ),
    "environment": (
        "noise_level",
        "distractions",
        "time_pressure",
        "context_stability",
        "visual_distraction",
        "interruption_risk",
        "social_pressure",
        "device_constraints",
        "lighting_quality",
        "mobility_context",
    ),
}

STATE_MODEL_KEYS = {
    "task": "task_model",
    "interface": "interface_model",
    "environment": "environment_model",
}


def _parse_numeric_value(value: Any) -> int:
    raw_value = value.get("value") if isinstance(value, Mapping) else value
    try:
        parsed = int(round(float(raw_value)))
    except (TypeError, ValueError) as exc:
        raise ValueError("Updated model values must be numeric.") from exc
    if not 0 <= parsed <= 100:
        raise ValueError("Updated model values must be between 0 and 100.")
    return parsed


def _simulation_plan_from_state(state: Mapping[str, Any]) -> SimulationPlanSchema | None:
    simulation_plan = state.get("simulation_plan")
    if simulation_plan is None:
        return None
    if isinstance(simulation_plan, SimulationPlanSchema):
        return simulation_plan
    return SimulationPlanSchema.model_validate(simulation_plan)


def _update_attribute_value(attribute: Any, value: int) -> dict:
    if isinstance(attribute, Mapping):
        updated = dict(attribute)
        updated["value"] = value
        return updated
    return {"value": value}


def update_scenario_model(
    model_type: str,
    updated_values: Mapping[str, Any],
    state: Mapping[str, Any],
) -> dict:
    if model_type == "user":
        raise ValueError("User Model cannot be updated within a scenario.")
    if model_type not in EDITABLE_MODEL_ATTRIBUTES:
        raise ValueError(f"Unsupported scenario model type: {model_type}")
    if not updated_values:
        raise ValueError("No updated values provided.")

    allowed_attributes = set(EDITABLE_MODEL_ATTRIBUTES[model_type])
    unknown_fields = sorted(set(updated_values) - allowed_attributes)
    if unknown_fields:
        raise ValueError(
            "Unknown or non-editable model fields: " + ", ".join(unknown_fields)
        )

    model_key = STATE_MODEL_KEYS[model_type]
    current_model = deepcopy(state.get(model_key) or {})
    if not current_model:
        raise ValueError(f"No existing {model_key} found in workflow state.")

    for attribute_id, value in updated_values.items():
        parsed_value = _parse_numeric_value(value)
        if attribute_id not in current_model:
            raise ValueError(
                f"Model field does not exist in current {model_type} model: "
                f"{attribute_id}"
            )
        current_model[attribute_id] = _update_attribute_value(
            current_model.get(attribute_id),
            parsed_value,
        )

    updated_state = dict(state)
    updated_state[model_key] = current_model

    task_model = (
        current_model
        if model_type == "task"
        else deepcopy(updated_state.get("task_model") or {})
    )
    interface_model = (
        current_model
        if model_type == "interface"
        else deepcopy(updated_state.get("interface_model") or {})
    )

    if task_model and interface_model:
        computed_parameters = build_computed_task_parameters(
            task_model,
            interface_model,
            _simulation_plan_from_state(updated_state),
        )
        updated_state["computed_parameters"] = computed_parameters.model_dump()

    return updated_state
