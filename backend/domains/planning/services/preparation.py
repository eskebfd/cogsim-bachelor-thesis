from backend.domains.models.services.simulation_models import build_simulation_model
from backend.domains.planning.services.computed_parameters import (
    build_computed_task_parameters,
)
from backend.domains.planning.services.simulation_plan import get_simulation_plan_or_none


def prepare_computed_parameters_and_simulation_model(state: dict) -> dict:
    """Build computed task parameters and deterministic simulation model."""
    simulation_plan = get_simulation_plan_or_none(state)
    computed_parameters = build_computed_task_parameters(
        state["task_model"],
        state["interface_model"],
        simulation_plan=simulation_plan,
    )
    simulation_model = build_simulation_model(state.get("user_model", {}))
    return {
        "computed_parameters": computed_parameters.model_dump(),
        "simulation_model": simulation_model.model_dump(),
        "current_stage": "computed_parameters",
    }
