import pytest

from backend.domains.scenario.services.model_update import update_scenario_model


def attribute(value: int) -> dict:
    return {
        "value": value,
        "scale_min_description": "niedrig",
        "scale_max_description": "hoch",
        "explanation": "Testwert",
        "confidence": "high",
    }


def workflow_state() -> dict:
    task_model = {
        "task_name": "Testaufgabe",
        "task_goal": "Testziel",
        "task_complexity": attribute(50),
        "number_of_steps": attribute(30),
        "reading_demand": attribute(40),
        "input_demand": attribute(45),
        "memory_demand": attribute(35),
        "decision_demand": attribute(30),
        "error_criticality": attribute(25),
        "steps": [],
        "assumptions": [],
    }
    interface_model = {
        "text_volume": attribute(40),
        "sentence_length": attribute(40),
        "word_difficulty": attribute(40),
        "technical_terms": attribute(40),
        "visual_clutter": attribute(30),
        "navigation_complexity": attribute(30),
        "accessibility_support": attribute(20),
        "feedback_quality": attribute(60),
        "assumptions": [],
    }
    environment_model = {
        "noise_level": attribute(20),
        "distractions": attribute(25),
        "time_pressure": attribute(30),
        "context_stability": attribute(70),
        "visual_distraction": attribute(20),
        "interruption_risk": attribute(20),
        "social_pressure": attribute(10),
        "device_constraints": attribute(15),
        "lighting_quality": attribute(80),
        "mobility_context": attribute(10),
        "assumptions": [],
    }
    return {
        "task_model": task_model,
        "interface_model": interface_model,
        "environment_model": environment_model,
        "user_model": {"reading_difficulty": attribute(60)},
        "computed_parameters": {},
        "simulation_plan": None,
    }


def test_task_model_can_be_updated_and_recomputes_parameters():
    state = workflow_state()

    updated = update_scenario_model(
        "task",
        {"number_of_steps": 90},
        state,
    )

    assert updated["task_model"]["number_of_steps"]["value"] == 90
    assert updated["computed_parameters"]["navigation_effort"]["value"] == 50


def test_interface_model_can_be_updated_and_recomputes_parameters():
    state = workflow_state()

    updated = update_scenario_model(
        "interface",
        {"text_volume": 80, "visual_clutter": 60},
        state,
    )

    assert updated["interface_model"]["text_volume"]["value"] == 80
    assert updated["interface_model"]["visual_clutter"]["value"] == 60
    assert updated["computed_parameters"]["text_complexity"]["value"] == 50
    assert updated["computed_parameters"]["navigation_effort"]["value"] == 40
    assert updated["task_model"] == state["task_model"]
    assert updated["environment_model"] == state["environment_model"]


def test_environment_model_can_be_updated_without_llm_call(monkeypatch):
    import backend.core.llm.client as llm_service

    monkeypatch.setattr(
        llm_service,
        "generate_environment_model",
        lambda *args, **kwargs: pytest.fail("LLM must not be called"),
    )
    state = workflow_state()

    updated = update_scenario_model(
        "environment",
        {"noise_level": 55},
        state,
    )

    assert updated["environment_model"]["noise_level"]["value"] == 55
    assert "computed_parameters" in updated
    assert updated["task_model"] == state["task_model"]
    assert updated["interface_model"] == state["interface_model"]


def test_user_model_cannot_be_updated():
    with pytest.raises(ValueError, match="User Model cannot be updated"):
        update_scenario_model(
            "user",
            {"reading_difficulty": 20},
            workflow_state(),
        )


def test_invalid_fields_are_rejected():
    with pytest.raises(ValueError, match="Unknown or non-editable"):
        update_scenario_model(
            "task",
            {"unknown_field": 20},
            workflow_state(),
        )


def test_values_outside_range_are_rejected():
    with pytest.raises(ValueError, match="between 0 and 100"):
        update_scenario_model(
            "interface",
            {"visual_clutter": 101},
            workflow_state(),
        )


def test_updated_values_do_not_mutate_original_state():
    state = workflow_state()

    updated = update_scenario_model(
        "task",
        {"task_complexity": 10},
        state,
    )

    assert state["task_model"]["task_complexity"]["value"] == 50
    assert updated["task_model"]["task_complexity"]["value"] == 10
