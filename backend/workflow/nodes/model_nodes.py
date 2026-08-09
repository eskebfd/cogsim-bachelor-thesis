from backend.workflow.state import CogSimState

from backend.core.logging.workflow_logging import log_duration
from backend.domains.planning.services.simulation_plan import (
    get_simulation_plan_or_none,
    prepare_simulation_plan_from_state,
)
from backend.domains.models.services.generation import (
    generate_base_models,
    generate_environment_model_data,
    generate_interface_model_data,
    generate_task_model_data,
)


def construct_base_models(state: CogSimState) -> dict:
    with log_duration(
        "node.construct_base_models",
        current_stage=state.get("current_stage", ""),
    ):
        return generate_base_models(
            scenario_context=state["scenario_context"],
            scenario_dimensions=state.get("dimensions", {}),
            revision_instruction=state.get("revision_instruction", ""),
            simulation_plan=prepare_simulation_plan_from_state(state),
            current_task_model=state.get("task_model") or None,
        )


def construct_task_model(state: CogSimState) -> dict:
    current_task_model = state.get("task_model") or {}
    is_review = state.get("current_stage") == "review_base_task"

    with log_duration(
        "node.construct_task_model",
        current_stage=state.get("current_stage", ""),
    ):
        task_model_data = generate_task_model_data(
            scenario_context=state["scenario_context"],
            scenario_dimensions=state.get("dimensions", {}),
            revision_instruction=state.get("revision_instruction", ""),
            simulation_plan=get_simulation_plan_or_none(state),
            current_task_model=current_task_model if is_review else None,
        )

    result = {"task_model": task_model_data}
    if is_review:
        result.update(
            {
                "computed_parameters": {},
                "simulation_model": {},
                "results": {},
                "simulation_results": {},
                "simulation_step": 0,
                "simulation_finished": False,
            }
        )
    return result


def construct_environment_model(state: CogSimState) -> dict:
    with log_duration(
        "node.construct_environment_model",
        current_stage=state.get("current_stage", ""),
    ):
        environment_model = generate_environment_model_data(
            scenario_context=state["scenario_context"],
            scenario_dimensions=state.get("dimensions", {}),
            revision_instruction=state.get("revision_instruction", ""),
            simulation_plan=get_simulation_plan_or_none(state),
        )
    return {"environment_model": environment_model}


def construct_interface_model(state: CogSimState) -> dict:
    with log_duration(
        "node.construct_interface_model",
        current_stage=state.get("current_stage", ""),
    ):
        interface_model = generate_interface_model_data(
            scenario_context=state["scenario_context"],
            scenario_dimensions=state.get("dimensions", {}),
            revision_instruction=state.get("revision_instruction", ""),
            simulation_plan=get_simulation_plan_or_none(state),
        )
    return {"interface_model": interface_model}
