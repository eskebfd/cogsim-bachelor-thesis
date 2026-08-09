import streamlit as st

from frontend.shared.services.workflow_api import run_simulation_from_models
from frontend.state import (
    apply_workflow_state,
    build_scenario_context,
    get_session_id,
)
from frontend.workflow.steps import RESULTS_STEP


def run_simulation_from_plan(*, rerun: bool = True) -> None:
    scenario_description = st.session_state.get("scenario_input", "")
    base_models = st.session_state.get("base_model_preview") or {}
    prepared = st.session_state.get("computed_parameters_preview") or {}
    backend_state = st.session_state.get("backend_state", {})
    simulation_plan = backend_state["simulation_plan"]
    evaluation_metrics = backend_state.get("evaluation_metrics") or {
        "selected_metrics": simulation_plan["evaluation_metrics"]
    }

    result = run_simulation_from_models(
        description=scenario_description,
        scenario_context=build_scenario_context(scenario_description),
        user_model=base_models.get("user_model", {}),
        user_models=base_models.get("user_models", {}),
        task_model=base_models.get("task_model", {}),
        interface_model=base_models.get("interface_model", {}),
        environment_model=base_models.get("environment_model", {}),
        computed_parameters=prepared.get("computed_parameters", {}),
        evaluation_metrics=evaluation_metrics,
        simulation_plan=simulation_plan,
        simulation_model=prepared.get("simulation_model", {}),
        evaluation_goal_selection=backend_state.get("evaluation_goal_selection"),
        session_id=get_session_id(),
    )
    apply_workflow_state(
        {**result, "current_stage": "simulation"},
        target_step=RESULTS_STEP,
    )
    if rerun:
        st.rerun()
