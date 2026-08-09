from backend.workflow.state import CogSimState
from backend.core.logging.workflow_logging import log_duration
from backend.domains.simulation.execution import (
    initial_simulation_state,
    run_simulation_from_state,
)


def initialize_simulation(state: CogSimState) -> dict:
    with log_duration(
        "node.initialize_simulation",
        current_stage=state.get("current_stage", ""),
    ):
        return initial_simulation_state()


def run_simulation_step(state: CogSimState) -> dict:
    with log_duration(
        "node.run_time_discrete_simulation",
        task_steps=len(state.get("task_model", {}).get("steps", [])),
    ):
        return run_simulation_from_state(state)


def log_state(state: CogSimState) -> dict:
    with log_duration(
        "node.log_state",
        timeline_entries=len(state.get("logs", [])),
    ):
        return {}


def check_finished(state: CogSimState) -> str:
    with log_duration(
        "node.check_finished",
        simulation_finished=state.get("simulation_finished", False),
    ):
        if state["simulation_finished"]:
            return "generate_results"

        return "run_simulation_step"
