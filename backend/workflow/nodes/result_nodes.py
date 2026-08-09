from backend.workflow.state import CogSimState
from backend.core.logging.workflow_logging import log_duration
from backend.domains.simulation.visualization import build_timeline_visualization


def generate_results(state: CogSimState) -> dict:
    with log_duration(
        "node.generate_results",
        timeline_entries=len(state.get("logs", [])),
    ):
        return {"results": state.get("results", {})}


def prepare_visualization(state: CogSimState) -> dict:
    with log_duration(
        "node.prepare_visualization",
        timeline_entries=len(state.get("logs", [])),
    ):
        return {
            "visualization": build_timeline_visualization(state.get("logs", []))
        }
