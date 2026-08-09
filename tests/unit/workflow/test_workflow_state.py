from typing import get_args

from backend.workflow.state import CogSimState, WorkflowStage


def test_cogsim_state_contains_review_fields():
    annotations = CogSimState.__annotations__

    assert "feedback_target" in annotations
    assert "feedback" in annotations
    assert "revision_instruction" in annotations
    assert "last_feedback" in annotations
    assert "simulation_results" in annotations


def test_cogsim_state_contains_core_model_fields():
    annotations = CogSimState.__annotations__

    assert "scenario_description" in annotations
    assert "scenario_context" in annotations
    assert "user_model" in annotations
    assert "user_models" in annotations
    assert "task_model" in annotations
    assert "environment_model" in annotations
    assert "computed_parameters" in annotations
    assert "evaluation_metrics" in annotations
    assert "simulation_plan" in annotations
    assert "dimensions" in annotations


def test_cogsim_state_uses_explicit_workflow_stage_names():
    assert "user_task_environment_models" in get_args(WorkflowStage)
    assert "computed_parameters" in get_args(WorkflowStage)
    assert "simulation" in get_args(WorkflowStage)
