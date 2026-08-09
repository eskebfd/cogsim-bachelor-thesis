from frontend.features.simulation import results as simulation_results
from frontend.features.simulation.formatting import task_step_display_label
from frontend.shared.ui import layout
from frontend.shared.ui.metric_cards import render_metric_card
from frontend.shared.ui.page_header import render_page_header
from frontend.shared.styles.loader import build_cogsim_css


def test_theme_loader_composes_cogsim_background_and_tokens():
    css = build_cogsim_css()

    assert css.startswith("<style>")
    assert "--cogsim-primary: #5B5BD6" in css
    assert "cogsim-background.svg" not in css
    assert "data:image/svg+xml;base64," in css
    assert ".st-key-workflow_stepper_v7" in css


def test_ui_layout_keeps_compatibility_exports():
    assert layout.render_page_header is render_page_header
    assert layout.render_metric_card is render_metric_card


def test_results_module_reexports_formatting_helpers():
    assert simulation_results.task_step_display_label is task_step_display_label
