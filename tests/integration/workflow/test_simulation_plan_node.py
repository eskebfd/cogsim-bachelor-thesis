from backend.workflow.nodes import model_nodes
from backend.domains.models.services import generation as generation_service
from backend.domains.evaluation.registries.metrics import (
    build_default_evaluation_metrics_selection,
)


class GeneratedModel:
    def __init__(self, name: str):
        self.name = name

    def model_dump(self) -> dict:
        return {"name": self.name}


def generator(**kwargs) -> GeneratedModel:
    return GeneratedModel("User Model")


def base_state() -> dict:
    return {
        "current_stage": "user_task_environment_models",
        "scenario_context": {
            "description": "Test scenario",
            "user_profiles": ["Generisch", "ADHS"],
        },
        "dimensions": {},
        "revision_instruction": "",
    }


def test_base_model_workflow_prepares_default_simulation_plan(monkeypatch):
    monkeypatch.setattr(
        generation_service,
        "BASE_MODEL_GENERATORS",
        {},
    )

    result = model_nodes.construct_base_models(base_state())

    assert result["user_model"]["user_type"] == "Generic"
    assert list(result["user_models"]) == ["generic", "adhd"]
    assert result["simulation_plan"]["evaluation_metrics"]


def test_base_model_workflow_prepares_plan_when_metrics_exist(monkeypatch):
    monkeypatch.setattr(
        generation_service,
        "BASE_MODEL_GENERATORS",
        {},
    )
    state = base_state()
    state["evaluation_metrics"] = (
        build_default_evaluation_metrics_selection(
            ["cognitive_load", "completion_time"]
        ).model_dump()
    )

    result = model_nodes.construct_base_models(state)

    assert result["user_model"]["user_type"] == "Generic"
    assert list(result["user_models"]) == ["generic", "adhd"]
    assert [
        profile["profile_id"]
        for profile in result["simulation_plan"]["selected_user_profiles"]
    ] == ["generic", "adhd"]
    assert [
        metric["metric_id"]
        for metric in result["simulation_plan"]["evaluation_metrics"]
    ] == ["cognitive_load", "completion_time"]


def test_base_model_generator_receives_optional_simulation_plan(monkeypatch):
    captured = {}

    def capturing_generator(**kwargs):
        captured.update(kwargs)
        return GeneratedModel("Task Model")

    monkeypatch.setattr(
        generation_service,
        "BASE_MODEL_GENERATORS",
        {"task_model": capturing_generator},
    )
    state = base_state()
    state["evaluation_metrics"] = (
        build_default_evaluation_metrics_selection(
            ["cognitive_load"]
        ).model_dump()
    )

    result = model_nodes.construct_base_models(state)

    assert result["task_model"] == {"name": "Task Model"}
    assert captured["simulation_plan"] is not None
    assert captured["simulation_plan"].evaluation_metrics[0].metric_id == (
        "cognitive_load"
    )


def test_plan_required_models_select_model_generators(monkeypatch):
    called = []

    def named_generator(**kwargs):
        called.append(kwargs["scenario_context"]["requested_model"])
        return GeneratedModel("Generated Model")

    def task_generator(**kwargs):
        kwargs["scenario_context"]["requested_model"] = "task"
        return named_generator(**kwargs)

    def user_generator(**kwargs):
        kwargs["scenario_context"]["requested_model"] = "user"
        return named_generator(**kwargs)

    monkeypatch.setattr(
        generation_service,
        "BASE_MODEL_GENERATORS",
        {
            "user_model": user_generator,
            "task_model": task_generator,
        },
    )
    state = base_state()
    state["evaluation_metrics"] = (
        build_default_evaluation_metrics_selection(
            ["completion_time"]
        ).model_dump()
    )

    result = model_nodes.construct_base_models(state)

    assert called == ["task"]
    assert "task_model" in result
    assert result["user_model"]["user_type"] == "Generic"
