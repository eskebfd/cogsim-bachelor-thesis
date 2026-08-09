from html import escape

import streamlit as st

from frontend.features.models.common import dataframe_height


def build_simulation_plan_review_data(simulation_plan: dict) -> dict:
    return {
        "selected_user_profiles": [
            {
                "Profile ID": profile.get("profile_id", ""),
                "Label": profile.get("label", ""),
                "Baseline": profile.get("is_baseline", False),
            }
            for profile in simulation_plan.get("selected_user_profiles", [])
        ],
        "evaluation_metrics": [
            {
                "Metric ID": metric.get("metric_id", ""),
                "Name": metric.get("name", ""),
                "Type": metric.get("metric_type", ""),
            }
            for metric in simulation_plan.get("evaluation_metrics", [])
        ],
        "required_models": [
            {
                "Model": model.get("model_type", ""),
                "Scope": model.get("instance_scope", ""),
                "Required": model.get("required", True),
            }
            for model in simulation_plan.get("required_models", [])
        ],
    }


def render_simulation_plan_review(simulation_plan: dict) -> dict:
    if not simulation_plan:
        st.warning("Es wurde noch kein Simulationsplan erstellt.")
        return {}

    review_data = build_simulation_plan_review_data(simulation_plan)
    sections = (
        ("Nutzerprofile", "selected_user_profiles"),
        ("Ausgewählte Auswertungswerte", "evaluation_metrics"),
        ("Verwendete Grundlagen", "required_models"),
    )
    for title, key in sections:
        rows = review_data[key]
        st.markdown(
            (
                '<div class="cogsim-plan-section-title">'
                f"{escape(title)}"
                "</div>"
            ),
            unsafe_allow_html=True,
        )
        if not rows:
            st.caption("Keine Einträge vorhanden.")
            continue

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
            height=dataframe_height(len(rows)),
        )

    return review_data
