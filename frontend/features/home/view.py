import streamlit as st

HOME_STEPS = [
    {
        "number": "01",
        "title": "Aufgabe beschreiben",
        "description": (
            "Beschreibe kurz, welche Aufgabe auf einer Website oder "
            "in einer Anwendung durchgeführt werden soll."
        ),
    },
    {
        "number": "02",
        "title": "Modelle überprüfen",
        "description": (
            "Prüfe die automatisch erstellten Modelle und passe sie "  "bei Bedarf an."
        ),
    },
    {
        "number": "03",
        "title": "Simulation starten",
        "description": ("Führe die Simulation für verschiedene Nutzerprofile aus."),
    },
    {
        "number": "04",
        "title": "Ergebnisse vergleichen",
        "description": (
            "Erkenne mögliche Schwierigkeiten und leite Verbesserungen "
            "für dein Interface ab."
        ),
    },
]


def _build_home_hero_html() -> str:
    return (
        '<div class="cogsim-home-hero">'
        '<div class="cogsim-home-eyebrow">COGSIM</div>'
        '<h1 class="cogsim-home-title">'
        "Cognitive Interaction Simulation"
        "</h1>"
        '<p class="cogsim-home-lead">'
        "CogSim hilft dabei, digitale Benutzeroberflächen aus der Sicht "
        "verschiedener Nutzerprofile zu untersuchen. Dafür beschreibst du "
        "einfach eine Aufgabe, die auf einer Website oder in einer Anwendung "
        "durchgeführt werden soll."
        "</p>"
        '<p class="cogsim-home-description">'
        "Aus deiner Beschreibung erstellt CogSim automatisch Modelle und "
        "simuliert, wie unterschiedliche Nutzerprofile die Aufgabe bearbeiten. "
        "Anschließend zeigt dir das Tool, wo Schwierigkeiten, Verzögerungen "
        "oder Unterschiede entstehen können. So kannst du dein Interface "
        "gezielt verbessern, bevor es final umgesetzt wird."
        "</p>"
        "</div>"
    )


def _build_home_step_html(
    number: str,
    title: str,
    description: str,
) -> str:
    return (
        '<div class="cogsim-home-step">'
        f'<div class="cogsim-home-step__number">{number}</div>'
        f'<div class="cogsim-home-step__title">{title}</div>'
        f'<div class="cogsim-home-step__description">{description}</div>'
        "</div>"
    )


def render_home_view() -> None:
    st.html(_build_home_hero_html())

    columns = st.columns(
        len(HOME_STEPS),
        gap="medium",
    )

    for column, step in zip(columns, HOME_STEPS):
        with column:
            st.html(
                _build_home_step_html(
                    number=step["number"],
                    title=step["title"],
                    description=step["description"],
                )
            )

    if st.button(
        "Neue Simulation starten",
        type="primary",
        use_container_width=False,
    ):
        st.session_state.current_view = "simulation"
        st.session_state.simulation_step = 1
        st.rerun()
