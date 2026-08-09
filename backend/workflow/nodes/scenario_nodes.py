from backend.workflow.state import CogSimState
from backend.core.logging.workflow_logging import log_duration
from backend.domains.scenario.services.dimensions import analyze_scenario_dimensions
from backend.core.llm.client import (
    extract_environment_dimension_signals as llm_extract_environment_dimension_signals,
    extract_interface_dimension_signals as llm_extract_interface_dimension_signals,
    extract_scenario_dimension_context as llm_extract_scenario_dimension_context,
    extract_task_dimension_signals as llm_extract_task_dimension_signals,
    merge_scenario_dimension_parts,
)


def extract_dimensions(state: CogSimState) -> dict:
    with log_duration(
        "node.extract_dimensions",
        current_stage=state.get("current_stage", ""),
    ):
        dimensions = analyze_scenario_dimensions(
            state["scenario_description"],
            state.get("scenario_image"),
        )

        scenario_context = state.get("scenario_context", {})
        scenario_context["description"] = state["scenario_description"]

        return {
            "dimensions": dimensions.model_dump(),
            "scenario_context": scenario_context,
            "current_stage": "dimensions",
            "scenario_image": None,
            "scenario_image_metadata": (
                dimensions.scenario_image_metadata.model_dump()
                if dimensions.scenario_image_metadata
                else None
            ),
            "multimodal_analysis": (
                dimensions.multimodal_analysis.model_dump()
                if dimensions.multimodal_analysis
                else None
            ),
        }


def extract_dimension_context(state: CogSimState) -> dict:
    with log_duration(
        "node.extract_dimension_context",
        current_stage=state.get("current_stage", ""),
    ):
        dimension_context = llm_extract_scenario_dimension_context(
            state["scenario_description"],
        )

        scenario_context = state.get("scenario_context", {})
        scenario_context["description"] = state["scenario_description"]

        return {
            "dimension_context": dimension_context.model_dump(),
            "scenario_context": scenario_context,
        }


def extract_task_dimension_signals(state: CogSimState) -> dict:
    with log_duration(
        "node.extract_task_dimension_signals",
        current_stage=state.get("current_stage", ""),
    ):
        task_signals = llm_extract_task_dimension_signals(
            state["scenario_description"],
            state["dimension_context"],
        )
        return {"task_dimension_signals": task_signals.model_dump()}


def extract_interface_dimension_signals(state: CogSimState) -> dict:
    with log_duration(
        "node.extract_interface_dimension_signals",
        current_stage=state.get("current_stage", ""),
    ):
        interface_signals = llm_extract_interface_dimension_signals(
            state["scenario_description"],
            state["dimension_context"],
        )
        return {"interface_dimension_signals": interface_signals.model_dump()}


def extract_environment_dimension_signals(state: CogSimState) -> dict:
    with log_duration(
        "node.extract_environment_dimension_signals",
        current_stage=state.get("current_stage", ""),
    ):
        environment_signals = llm_extract_environment_dimension_signals(
            state["scenario_description"],
            state["dimension_context"],
        )
        return {"environment_dimension_signals": environment_signals.model_dump()}


def merge_dimension_signals(state: CogSimState) -> dict:
    with log_duration(
        "node.merge_dimension_signals",
        current_stage=state.get("current_stage", ""),
    ):
        dimensions = merge_scenario_dimension_parts(
            state["dimension_context"],
            state["task_dimension_signals"],
            state["interface_dimension_signals"],
            state["environment_dimension_signals"],
        )

        return {
            "dimensions": dimensions.model_dump(),
            "current_stage": "dimensions",
            "scenario_image": None,
            "scenario_image_metadata": None,
            "multimodal_analysis": None,
        }
