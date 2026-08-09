import streamlit as st

from frontend.features.models.actions import prepare_simulation
from frontend.shared.ui.loading_overlay import global_loading
from frontend.workflow.review_action_panel import (
    render_review_action_panel,
)
from frontend.workflow.step_navigation import (
    render_step_navigation,
)
from frontend.features.models.view import (
    render_simulation_foundations_view,
)
from frontend.features.evaluation_goals.view import (
    render_metrics_setup_view,
)
from frontend.features.simulation.view import render_results_view
from frontend.features.computed_parameters.view import render_simulation_plan_view
from frontend.features.scenario.view import (
    render_scenario_input_view,
)
from frontend.features.task_flow.view import (
    render_task_flow_view,
)
from frontend.features.dimensions.view import (
    render_scenario_setup_view,
)
from frontend.features.user_profiles.view import (
    render_user_profiles_view,
)
from frontend.workflow.steps import (
    DIMENSIONS_STEP,
    METRICS_STEP,
    RESULTS_STEP,
    SCENARIO_STEP,
    SIMULATION_FOUNDATIONS_STEP,
    SIMULATION_PLAN_STEP,
    TASK_FLOW_STEP,
    USER_PROFILES_STEP,
)


def handle_pending_workflow_actions() -> None:
    if st.session_state.pop("pending_simulation_preparation", False):
        with global_loading(
            "Der Simulationsplan wird vorbereitet.",
            hint="Die aktuell geprüften Werte werden übernommen.",
            estimated_seconds=18.0,
        ):
            prepare_simulation(rerun=False)


def render_current_step() -> None:
    current_step = st.session_state.get(
        "simulation_step",
        1,
    )

    if current_step == USER_PROFILES_STEP:
        render_user_profiles_view()

    elif current_step == METRICS_STEP:
        render_metrics_setup_view()

    elif current_step == SCENARIO_STEP:
        render_scenario_input_view()

    elif current_step == TASK_FLOW_STEP:
        render_task_flow_view()

    elif current_step == DIMENSIONS_STEP:
        render_scenario_setup_view()

    elif current_step == SIMULATION_FOUNDATIONS_STEP:
        render_simulation_foundations_view()

    elif current_step == SIMULATION_PLAN_STEP:
        render_simulation_plan_view()

    elif current_step == RESULTS_STEP:
        render_results_view()


def render_workflow_view() -> None:
    handle_pending_workflow_actions()

    st.markdown(
        '<div class="cogsim-workflow-eyebrow">Simulation</div>',
        unsafe_allow_html=True,
    )

    render_step_navigation()
    render_current_step()

    render_review_action_panel(
        st.session_state.get(
            "simulation_step",
            1,
        )
    )
