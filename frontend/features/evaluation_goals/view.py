import streamlit as st

from frontend.features.evaluation_goals.section import (
    render_metrics_section,
)
from frontend.shared.ui.page_header import (
    render_page_header,
)
from frontend.workflow.actions import (
    go_to_step,
    update_modeling_setup_state,
)


def render_metrics_setup_view() -> None:
    render_page_header(
        "Auswertung",
        "",
        icon="bar-chart-3",
    )

    dimensions = st.session_state.get("dimensions") or {}

    evaluation_selection = render_metrics_section(dimensions)

    evaluation_goal_selection = evaluation_selection["evaluation_goal_selection"]

    evaluation_metrics = evaluation_selection["evaluation_metrics"]

    st.session_state.evaluation_goal_selection = evaluation_goal_selection

    st.session_state.evaluation_metrics = evaluation_metrics
    has_selected_metrics = bool(
        (evaluation_metrics or {}).get("selected_metrics")
    )

    scenario_description = st.session_state.get(
        "scenario_input",
        "",
    )

    update_modeling_setup_state(
        scenario_description,
        dimensions,
        evaluation_goal_selection=(evaluation_goal_selection),
        evaluation_metrics=evaluation_metrics,
        clear_evaluation_selection=not has_selected_metrics,
    )

    st.write("")

    if not has_selected_metrics:
        st.info(
            "Wähle mindestens einen Kennwert aus, damit CogSim weiß, "
            "worauf die spätere Auswertung achten soll."
        )

    if st.button(
        "Weiter zum Szenario",
        type="primary",
        use_container_width=True,
        disabled=not has_selected_metrics,
    ):
        go_to_step(3)
