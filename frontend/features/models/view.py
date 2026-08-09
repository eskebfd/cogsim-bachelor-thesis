from frontend.features.models.simulation_foundations import (
    render_simulation_foundations_section,
)
from frontend.shared.ui.page_header import render_page_header


def render_simulation_foundations_view() -> None:
    render_page_header(
        "Simulationsgrundlagen",
        "",
        icon="boxes",
    )

    render_simulation_foundations_section()
