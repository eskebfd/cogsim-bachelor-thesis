import streamlit as st

from frontend.shared.services.workflow_api import fetch_scenario_dimensions
from frontend.state import (
    build_scenario_context,
    get_session_id,
    apply_workflow_state,
    update_backend_state,
)


def go_to_step(step: int) -> None:
    st.session_state.simulation_step = step
    st.rerun()


def clear_model_outputs() -> None:
    st.session_state.base_model_preview = None
    st.session_state.computed_parameters_preview = None
    st.session_state.simulation_result = None


def go_home() -> None:
    st.session_state.current_view = "home"
    st.rerun()


def analyze_scenario_dimensions(
    scenario_description: str,
    scenario_image: dict | None = None,
) -> dict:
    result = fetch_scenario_dimensions(
        description=scenario_description,
        session_id=get_session_id(),
        scenario_image=scenario_image,
        task_model=(st.session_state.get("base_model_preview") or {}).get(
            "task_model"
        )
        or (st.session_state.get("backend_state") or {}).get("task_model"),
    )

    apply_workflow_state(
        {
            **result,
            "current_stage": "dimensions",
            "scenario_description": scenario_description,
            "scenario_text": scenario_description,
            "scenario_image_metadata": result.get("scenario_image_metadata"),
            "multimodal_analysis": result.get("multimodal_analysis"),
            "session_id": get_session_id(),
            "scenario_context": result.get(
                "scenario_context",
                build_scenario_context(scenario_description),
            ),
            "dimensions": result.get("dimensions", result),
        }
    )

    return st.session_state.dimensions


def update_modeling_setup_state(
    scenario_description: str,
    dimensions: dict,
    evaluation_goal_selection: dict | None = None,
    evaluation_metrics: dict | None = None,
    clear_evaluation_selection: bool = False,
) -> None:
    updates = dict(
        current_stage="modeling_setup",
        scenario_description=scenario_description,
        session_id=get_session_id(),
        scenario_context=build_scenario_context(scenario_description),
        dimensions=dimensions,
    )
    if clear_evaluation_selection:
        updates["evaluation_goal_selection"] = None
        updates["evaluation_metrics"] = None
        updates["simulation_plan"] = None
        updates["computed_parameters"] = {}
    elif evaluation_goal_selection is not None:
        updates["evaluation_goal_selection"] = evaluation_goal_selection
    elif evaluation_metrics is not None:
        updates["evaluation_goal_selection"] = None
    if evaluation_metrics is not None:
        updates["evaluation_metrics"] = evaluation_metrics
        updates["simulation_plan"] = None
        updates["computed_parameters"] = {}
    update_backend_state(**updates)
