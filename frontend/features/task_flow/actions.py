import streamlit as st

from frontend.shared.services.workflow_api import (
    generate_task_flow_workflow,
)
from frontend.shared.ui.loading_overlay import global_loading
from frontend.state import (
    apply_workflow_state,
    build_scenario_context,
    get_session_id,
)


def generate_task_flow_with_progress(scenario_description: str) -> dict:
    scenario_context = build_scenario_context(scenario_description)
    backend_state = st.session_state.get("backend_state", {})

    try:
        with global_loading(
            "Der Aufgabenablauf wird erstellt.",
            hint="Die Arbeitsschritte und Zeiten werden aus dem Szenario abgeleitet.",
            estimated_seconds=30.0,
        ):
            result = generate_task_flow_workflow(
                description=scenario_description,
                scenario_context=scenario_context,
                session_id=get_session_id(),
                evaluation_goal_selection=backend_state.get(
                    "evaluation_goal_selection"
                ),
                evaluation_metrics=backend_state.get("evaluation_metrics"),
                simulation_plan=backend_state.get("simulation_plan"),
            )
    except RuntimeError as exc:
        st.error(
            "Der Aufgabenablauf konnte nicht erstellt werden. "
            f"{exc}"
        )
        return {}

    apply_workflow_state(
        {
            **result,
            "current_stage": "task_model",
            "scenario_description": scenario_description,
            "session_id": get_session_id(),
            "scenario_context": result.get("scenario_context", scenario_context),
            "dimensions": st.session_state.get("dimensions") or {},
        },
        target_step=4,
        invalidate_downstream=True,
    )

    return (st.session_state.get("base_model_preview") or {}).get("task_model") or {}
