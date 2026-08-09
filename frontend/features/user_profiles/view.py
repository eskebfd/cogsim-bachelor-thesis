import streamlit as st

from frontend.workflow.actions import clear_model_outputs, go_to_step
from frontend.features.user_profiles.section import (
    PROFILE_SELECTION_CHANGED_FLAG,
    render_user_profiles_section,
)
from frontend.shared.ui.page_header import render_page_header
from frontend.state import update_backend_state


def render_user_profiles_view() -> None:
    render_page_header(
        "Nutzerprofile auswählen",
        "",
    )

    previous_profiles = st.session_state.get(
        "user_profiles",
        [],
    )

    profiles = render_user_profiles_section()

    selection_changed = st.session_state.pop(
        PROFILE_SELECTION_CHANGED_FLAG,
        False,
    )

    if profiles != previous_profiles or selection_changed:
        clear_model_outputs()

    st.session_state.user_profiles = profiles
    st.session_state.user_profile = ", ".join(profiles)
    st.session_state.comparison_baseline = "Generisch"

    context = st.session_state.get(
        "backend_state",
        {},
    ).get(
        "scenario_context",
        {},
    )

    update_backend_state(
        scenario_context={
            **context,
            "user_profiles": profiles,
            "user_profile": st.session_state.user_profile,
            "comparison_baseline": "Generisch",
        },
        user_model={},
        user_models={},
        simulation_plan=None,
        computed_parameters={},
        simulation_results={},
    )

    st.write("")

    if st.button(
        "Weiter zur Auswertung",
        type="primary",
        use_container_width=True,
    ):
        go_to_step(2)
