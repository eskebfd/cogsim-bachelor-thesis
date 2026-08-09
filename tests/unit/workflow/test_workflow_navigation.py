import frontend.workflow.step_navigation as step_navigation
from frontend.workflow.steps import (
    RESULTS_STEP,
    SIMULATION_FOUNDATIONS_STEP,
    WORKFLOW_STEP_DEFINITIONS,
    workflow_step_by_number,
)


def test_stepper_contains_eight_numbered_steps_with_task_flow_review():
    assert step_navigation.WORKFLOW_STEPS == [
        (1, "Nutzerprofile"),
        (2, "Auswertung"),
        (3, "Szenario"),
        (4, "Aufgabenablauf"),
        (5, "Anforderungen"),
        (6, "Simulationsgrundlagen"),
        (7, "Simulationsplan"),
        (8, "Ergebnisse"),
    ]


def test_workflow_steps_define_ids_and_features_centrally():
    assert workflow_step_by_number(SIMULATION_FOUNDATIONS_STEP).step_id == (
        "simulation_foundations"
    )
    assert workflow_step_by_number(RESULTS_STEP).feature == "simulation"
    assert [step.number for step in WORKFLOW_STEP_DEFINITIONS] == list(range(1, 9))


def test_workflow_steps_document_state_requirements():
    results_step = workflow_step_by_number(RESULTS_STEP)
    foundations_step = workflow_step_by_number(SIMULATION_FOUNDATIONS_STEP)

    assert results_step.description
    assert results_step.required_state_keys == ("simulation_result",)
    assert foundations_step.required_state_keys == (
        "dimensions",
        "base_model_preview",
    )


def test_stepper_uses_reduced_state_model():
    assert step_navigation._step_state(3, 3) == "active"
    assert step_navigation._step_state(2, 3) == "completed"
    assert step_navigation._step_state(4, 3) == "upcoming"


def test_reduced_stepper_no_longer_exports_gating_helpers():
    assert not hasattr(step_navigation, "workflow_step_is_enabled")
    assert not hasattr(step_navigation, "workflow_step_is_clickable")
