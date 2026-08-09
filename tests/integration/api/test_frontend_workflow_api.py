import pytest

import frontend.shared.services.workflow_api as workflow_api


class FakeResponse:
    def __init__(self, payload, status_code=200, text=None):
        self.payload = payload
        self.status_code = status_code
        self.ok = 200 <= status_code < 400
        self.text = text if text is not None else str(payload)

    def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


def test_post_json_reports_backend_json_error(monkeypatch):
    monkeypatch.setattr(
        workflow_api.requests,
        "post",
        lambda *args, **kwargs: FakeResponse(
            {
                "status": "error",
                "error_type": "ValidationError",
                "message": "noise_level has no numeric value",
                "workflow_step": "scenario_dimensions",
            },
            status_code=500,
        ),
    )

    with pytest.raises(RuntimeError, match="noise_level has no numeric value"):
        workflow_api.post_json("http://backend", {})


def test_post_json_reports_non_json_response(monkeypatch):
    monkeypatch.setattr(
        workflow_api.requests,
        "post",
        lambda *args, **kwargs: FakeResponse(
            ValueError("invalid JSON"),
            text="Internal Server Error",
        ),
    )

    with pytest.raises(RuntimeError, match="Internal Server Error"):
        workflow_api.post_json("http://backend", {})


def test_fetch_scenario_dimensions_posts_memory_payload(monkeypatch):
    calls = []

    def fake_post(url, json, timeout):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse({"dimensions": {"user_profile": "ADHS"}})

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    result = workflow_api.fetch_scenario_dimensions(
        description="Test scenario",
        session_id="session-1",
    )

    assert result == {"dimensions": {"user_profile": "ADHS"}}
    assert calls[0]["json"]["session_id"] == "session-1"
    assert calls[0]["url"] == workflow_api.WORKFLOW_DISPATCH_URL
    assert calls[0]["json"]["command"] == "analyze_dimensions"
    assert calls[0]["json"]["payload"]["description"] == "Test scenario"


def test_analyze_screenshot_task_structure_posts_image_only_payload(monkeypatch):
    calls = []

    def fake_post(url, json, timeout):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse(
            {
                "screenshot_task_analysis": {
                    "user_goal": "Unterkunft auswählen",
                    "main_task": "Hotel prüfen",
                    "task_description": "Die Person prüft ein Hotelangebot.",
                    "interface_description": "Die Oberfläche zeigt Hotelkarten.",
                    "hta_steps": [],
                    "decision_points": [],
                    "interface_elements": [],
                    "visible_elements": [],
                    "uncertainties": [],
                    "missing_information": [],
                    "warning": None,
                }
            }
        )

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    result = workflow_api.analyze_screenshot_task_structure(
        {"filename": "screen.png"},
        session_id="session-1",
    )

    assert result["screenshot_task_analysis"]["main_task"] == "Hotel prüfen"
    assert result["screenshot_task_analysis"]["interface_description"] == (
        "Die Oberfläche zeigt Hotelkarten."
    )
    assert calls[0]["json"]["session_id"] == "session-1"
    assert calls[0]["json"]["command"] == "analyze_screenshot"
    assert calls[0]["json"]["payload"] == {
        "scenario_image": {"filename": "screen.png"}
    }


def test_generate_user_task_environment_models_workflow_uses_typed_payload(
    monkeypatch,
):
    calls = []

    def fake_post(url, json, timeout):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse({"current_stage": "user_task_environment_models"})

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    workflow_api.generate_user_task_environment_models_workflow(
        description="Test scenario",
        scenario_context={"description": "Test scenario"},
        dimensions={"detected_user": "ADHS"},
        session_id="session-1",
    )

    assert calls[0]["json"]["command"] == "generate_base_models"
    assert calls[0]["json"]["payload"] == {
        "description": "Test scenario",
        "scenario_description": "Test scenario",
        "scenario_context": {"description": "Test scenario"},
        "dimensions": {"detected_user": "ADHS"},
    }


def test_existing_frontend_payloads_do_not_require_evaluation_metrics(
    monkeypatch,
):
    calls = []

    def fake_post(url, json, timeout):
        calls.append(json)
        return FakeResponse({"current_stage": "dimensions"})

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    workflow_api.fetch_scenario_dimensions("Test scenario")

    assert "evaluation_metrics" not in calls[0]["payload"]


def test_frontend_payload_serializes_simulation_plan_when_provided(monkeypatch):
    calls = []
    plan = {"selected_user_profiles": [{"profile_id": "generic"}]}

    def fake_post(url, json, timeout):
        calls.append(json)
        return FakeResponse({"current_stage": "dimensions"})

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    workflow_api.fetch_scenario_dimensions(
        "Test scenario",
        simulation_plan=plan,
    )

    assert calls[0]["payload"]["simulation_plan"] == plan


def test_base_model_payload_serializes_evaluation_metrics_when_provided(
    monkeypatch,
):
    calls = []
    selection = {"selected_metrics": [{"metric_id": "cognitive_load"}]}

    def fake_post(url, json, timeout):
        calls.append(json)
        return FakeResponse({"current_stage": "user_task_environment_models"})

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    workflow_api.generate_user_task_environment_models_workflow(
        description="Test scenario",
        scenario_context={"user_profiles": ["Generisch"]},
        dimensions={},
        evaluation_metrics=selection,
    )

    assert calls[0]["payload"]["evaluation_metrics"] == selection


def test_update_scenario_model_workflow_transfers_updated_values(monkeypatch):
    calls = []

    def fake_post(url, json, timeout):
        calls.append(json)
        return FakeResponse({"task_model": {"number_of_steps": {"value": 80}}})

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    workflow_api.update_scenario_model_workflow(
        description="Test scenario",
        scenario_context={"description": "Test scenario"},
        user_model={"name": "User Model"},
        task_model={"number_of_steps": {"value": 20}},
        interface_model={"visual_clutter": {"value": 30}},
        environment_model={"noise_level": {"value": 10}},
        model_type="task",
        updated_values={"number_of_steps": 80},
        simulation_plan={"selected_user_profiles": []},
    )

    assert calls[0]["command"] == "update_scenario_model"
    assert calls[0]["payload"]["model_type"] == "task"
    assert calls[0]["payload"]["updated_values"] == {"number_of_steps": 80}


def test_prepare_simulation_workflow_dispatches_single_command(
    monkeypatch,
):
    calls = []

    def fake_post(url, json, timeout):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse(
            {
                "current_stage": "computed_parameters",
                "computed_parameters": {},
            }
        )

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    result = workflow_api.prepare_simulation_workflow(
        description="Test scenario",
        scenario_context={"description": "Test scenario"},
        user_model={"name": "User Model"},
        task_model={"name": "Task Model"},
        interface_model={"name": "Interface Model"},
        environment_model={"name": "Environment Model"},
        evaluation_metrics={"selected_metrics": []},
        simulation_plan={"selected_user_profiles": []},
        session_id="session-1",
    )

    assert result["current_stage"] == "computed_parameters"
    assert calls[0]["url"] == workflow_api.WORKFLOW_DISPATCH_URL
    assert calls[0]["json"]["session_id"] == "session-1"
    assert calls[0]["json"]["command"] == "prepare_simulation"
    assert calls[0]["json"]["payload"]["user_model"] == {"name": "User Model"}
    assert calls[0]["json"]["payload"]["task_model"] == {"name": "Task Model"}
    assert calls[0]["json"]["payload"]["interface_model"] == {
        "name": "Interface Model"
    }
    assert calls[0]["json"]["payload"]["environment_model"] == {
        "name": "Environment Model"
    }


def test_review_base_model_posts_review_payload(monkeypatch):
    calls = []

    def fake_post(url, json, timeout):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse({"user_model": {}})

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    workflow_api.review_base_model(
        description="Test scenario",
        scenario_context={"description": "Test scenario"},
        user_model={},
        task_model={},
        interface_model={},
        environment_model={},
        feedback_target="user_model",
        feedback={"summary": "Bitte überarbeiten"},
        session_id="session-1",
    )

    assert calls[0]["url"] == workflow_api.WORKFLOW_DISPATCH_URL
    assert calls[0]["json"]["command"] == "review_base_model"
    assert calls[0]["json"]["payload"]["feedback_target"] == "user_model"
    assert calls[0]["json"]["payload"]["feedback"] == {
        "summary": "Bitte überarbeiten"
    }


def test_run_simulation_from_models_dispatches_single_command(monkeypatch):
    calls = []

    def fake_post(url, json, timeout):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse({"results": {"completed": True}})

    monkeypatch.setattr(workflow_api.requests, "post", fake_post)

    result = workflow_api.run_simulation_from_models(
        description="Test scenario",
        scenario_context={"description": "Test scenario"},
        user_model={},
        task_model={},
        interface_model={},
        environment_model={},
        computed_parameters={"text_complexity": {"value": 30}},
        evaluation_metrics={"selected_metrics": []},
        simulation_plan={"selected_user_profiles": []},
        simulation_model={"time_step_seconds": 2},
        session_id="session-1",
    )

    assert result == {"results": {"completed": True}}
    assert calls[0]["url"] == workflow_api.WORKFLOW_DISPATCH_URL
    assert calls[0]["json"]["command"] == "run_simulation"
    assert calls[0]["json"]["payload"]["description"] == "Test scenario"
    assert calls[0]["json"]["payload"]["simulation_model"] == {
        "time_step_seconds": 2
    }
