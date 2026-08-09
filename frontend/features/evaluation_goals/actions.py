import streamlit as st

from frontend.shared.services.workflow_api import (
    generate_user_task_environment_models_workflow,
)
from frontend.shared.ui.loading_overlay import global_loading
from frontend.state import (
    apply_workflow_state,
    get_session_id,
    build_scenario_context,
)


def generate_base_models_with_progress(scenario_description: str) -> dict:
    scenario_context = build_scenario_context(scenario_description)

    try:
        with global_loading(
            "Die Modelle für das Szenario werden erstellt.",
            hint="Aufgabe, Interface und Umgebung werden vorbereitet.",
            estimated_seconds=45.0,
        ):
            backend_state = st.session_state.get("backend_state", {})
            result = generate_user_task_environment_models_workflow(
                description=scenario_description,
                scenario_context=scenario_context,
                dimensions=st.session_state.get("dimensions") or {},
                session_id=get_session_id(),
                task_model=(st.session_state.get("base_model_preview") or {}).get(
                    "task_model"
                )
                or backend_state.get("task_model"),
                evaluation_goal_selection=backend_state.get(
                    "evaluation_goal_selection"
                ),
                evaluation_metrics=backend_state.get("evaluation_metrics"),
                simulation_plan=backend_state.get("simulation_plan"),
            )
    except RuntimeError as exc:
        st.error(
            "Die Modelle konnten nicht erstellt werden. "
            f"{exc}"
        )
        return {}

    apply_workflow_state(
        {
            **result,
            "current_stage": "user_task_environment_models",
            "scenario_description": scenario_description,
            "session_id": get_session_id(),
            "scenario_context": result.get("scenario_context", scenario_context),
            "dimensions": result.get(
                "dimensions",
                st.session_state.get("dimensions") or {},
            ),
        }
    )

    return st.session_state.base_model_preview or {}
