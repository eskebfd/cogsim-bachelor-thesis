from html import escape

import streamlit as st


def _render_inline_list(
    title: str,
    values: list[str],
) -> None:
    if not values:
        return

    st.markdown(f"**{title}:** {', '.join(values)}")


def _render_screenshot_task_analysis(
    analysis: dict | None,
) -> None:
    if not analysis:
        return

    warning = analysis.get("warning")

    user_goal = analysis.get("user_goal")
    main_task = analysis.get("main_task")
    hta_steps = analysis.get("hta_steps") or []
    interface_elements = analysis.get("interface_elements") or []
    decision_points = analysis.get("decision_points") or []
    missing_information = analysis.get("missing_information") or []

    with st.container(
        border=True,
        key="screenshot_analysis_result",
    ):
        st.markdown(
            (
                '<div class="cogsim-screenshot-analysis__header">'
                '<div class="cogsim-screenshot-analysis__eyebrow">'
                "Analyse abgeschlossen"
                "</div>"
                '<div class="cogsim-screenshot-analysis__title">'
                "Erkannte Hinweise aus dem Screenshot"
                "</div>"
                '<div class="cogsim-screenshot-analysis__copy">'
                "Die folgenden Punkte sind plausible Annahmen für die spätere "
                "HTA-Struktur."
                "</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        if warning:
            st.warning(warning)


        if user_goal or main_task:
            summary_cards = []

            if user_goal:
                summary_cards.append(
                    (
                        '<div class="cogsim-screenshot-summary-card">'
                        '<div class="cogsim-screenshot-summary-card__label">'
                        "Nutzerziel"
                        "</div>"
                        '<div class="cogsim-screenshot-summary-card__value">'
                        f"{escape(user_goal)}"
                        "</div>"
                        "</div>"
                    )
                )

            if main_task:
                summary_cards.append(
                    (
                        '<div class="cogsim-screenshot-summary-card">'
                        '<div class="cogsim-screenshot-summary-card__label">'
                        "Hauptaufgabe"
                        "</div>"
                        '<div class="cogsim-screenshot-summary-card__value">'
                        f"{escape(main_task)}"
                        "</div>"
                        "</div>"
                    )
                )

            st.markdown(
                (
                    '<div class="cogsim-screenshot-summary-grid">'
                    + "".join(summary_cards)
                    + "</div>"
                ),
                unsafe_allow_html=True,
            )


        if hta_steps:
            st.markdown(
                (
                    '<div class="cogsim-screenshot-analysis__section-title">'
                    "Mögliche Aufgabenstruktur"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

            for step in hta_steps:
                number = step.get("number", "")
                title = step.get("title", "")

                step_label = f"{number}. {title}" if number else title

                st.markdown(
                    f"""
                    <div class="cogsim-hta-step">
                        <span class="cogsim-hta-step__number">
                            {escape(str(number))}
                        </span>
                        <span class="cogsim-hta-step__title">
                            {escape(title or step_label)}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


        details_available = any(
            (
                interface_elements,
                decision_points,
                missing_information,
                any(
                    step.get("description")
                    or step.get("subtasks")
                    or step.get("interface_elements")
                    for step in hta_steps
                ),
            )
        )

        if not details_available:
            return

        with st.expander(
            "Weitere Analyseinformationen",
            expanded=False,
        ):
            detailed_steps = [
                step
                for step in hta_steps
                if (
                    step.get("description")
                    or step.get("subtasks")
                    or step.get("interface_elements")
                )
            ]

            if detailed_steps:
                st.markdown("**HTA-Schritte im Detail**")

                for step in detailed_steps:
                    number = step.get("number", "")
                    title = step.get("title", "")

                    step_label = f"{number}. {title}" if number else title

                    st.markdown(f"**{step_label}**")

                    description = step.get("description")
                    if description:
                        st.caption(description)

                    subtasks = step.get("subtasks") or []
                    if subtasks:
                        _render_inline_list(
                            "Teilaufgaben",
                            subtasks,
                        )

                    elements = step.get("interface_elements") or []
                    if elements:
                        _render_inline_list(
                            "Interface-Elemente",
                            elements,
                        )

            if interface_elements:
                st.markdown("---")
                _render_inline_list(
                    "Sichtbare Interface-Elemente",
                    interface_elements,
                )

            if decision_points:
                st.markdown("**Entscheidungspunkte**")

                for point in decision_points:
                    st.markdown(f"- {point}")

            if missing_information:
                st.markdown("**Noch unklar**")

                for item in missing_information:
                    st.markdown(f"- {item}")
