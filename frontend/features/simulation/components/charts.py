import streamlit as st

from frontend.features.simulation.components.data import (
    build_event_summary_rows,
    build_metric_chart_rows,
    build_overview_duration_chart_rows,
    build_overview_metric_chart_rows,
    build_task_duration_chart_rows,
    selected_metric_ids_from_session,
)


def render_overview_charts(profiles: list[dict]) -> None:
    metric_rows = build_overview_metric_chart_rows(profiles)
    duration_rows = build_overview_duration_chart_rows(profiles)

    metric_column, duration_column = st.columns(2)
    with metric_column:
        st.markdown("#### Vergleich der Profile")
        st.bar_chart(
            metric_rows,
            x="Profil",
            y=[
                "Cognitive Load",
                "Error Risk Score",
                "Task Success Score",
                "Completion Efficiency",
            ],
            height=320,
        )

    with duration_column:
        st.markdown("#### Dauer und kritische Ereignisse")
        st.bar_chart(
            duration_rows,
            x="Profil",
            y=["Completion Time (s)", "Events"],
            height=320,
        )


def render_profile_charts(profile: dict) -> None:
    metrics = profile.get("metrics", {})
    metric_rows = build_metric_chart_rows(
        metrics,
        selected_metric_ids_from_session(),
    )
    duration_rows = build_task_duration_chart_rows(profile)
    event_rows = build_event_summary_rows(profile)

    metric_column, event_column = st.columns(2)
    with metric_column:
        st.markdown("#### Ergebniswerte")
        if metric_rows:
            st.bar_chart(
                metric_rows,
                x="Metrik",
                y="Wert",
                height=300,
            )
        else:
            st.caption("Keine Ergebniswerte vorhanden.")

    with event_column:
        st.markdown("#### Kritische Ereignisse")
        if event_rows:
            st.bar_chart(
                event_rows,
                x="Event",
                y="Anzahl",
                height=300,
            )
        else:
            st.caption("Keine auffälligen Situationen markiert.")

    if duration_rows:
        st.markdown("#### Dauer der Arbeitsschritte")
        st.bar_chart(
            duration_rows,
            x="Task Step",
            y=["Geplant (s)", "Tatsächlich (s)", "Verzögerung (s)"],
            height=340,
        )
