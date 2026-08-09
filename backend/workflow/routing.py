from backend.workflow.state import CogSimState


def update_state_router(state: CogSimState) -> str:
    current_stage = state.get("current_stage", "")

    if current_stage == "dimensions":
        if state.get("scenario_image"):
            return "extract_dimensions"
        return "extract_dimension_context"

    if current_stage in ["user_task_environment_models", "base_models"]:
        return "construct_base_models"

    if current_stage == "task_model":
        return "construct_task_model"

    if current_stage == "interface_model":
        return "construct_interface_model"

    if current_stage == "environment_model":
        return "construct_environment_model"

    if current_stage == "computed_parameters":
        return "construct_computed_parameters"

    if current_stage.startswith("review_base"):
        return "prepare_revision_instruction"

    if current_stage == "simulation":
        return "initialize_simulation"

    return "finished"


def route_after_revision_instruction(state: CogSimState) -> str:
    current_stage = state.get("current_stage", "")

    if current_stage == "review_base_task":
        return "construct_task_model"

    if current_stage == "review_base_interface":
        return "construct_interface_model"

    if current_stage == "review_base_environment":
        return "construct_environment_model"

    return "finished"


def route_after_task_model(state: CogSimState) -> str:
    current_stage = state.get("current_stage", "")

    if current_stage in [
        "user_task_environment_models",
        "base_models",
    ]:
        return "construct_interface_model"

    return "finished"


def route_after_interface_model(state: CogSimState) -> str:
    current_stage = state.get("current_stage", "")

    if current_stage in [
        "user_task_environment_models",
        "base_models",
    ]:
        return "construct_environment_model"

    return "finished"
