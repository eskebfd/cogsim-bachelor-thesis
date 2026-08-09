from backend.workflow.state import CogSimState
from backend.core.logging.workflow_logging import log_duration
from backend.domains.planning.services.preparation import (
    prepare_computed_parameters_and_simulation_model,
)


def construct_computed_parameters(state: CogSimState) -> dict:
    with log_duration(
        "node.construct_computed_parameters",
        current_stage=state.get("current_stage", ""),
    ):
        return prepare_computed_parameters_and_simulation_model(state)
