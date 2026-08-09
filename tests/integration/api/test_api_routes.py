import pytest
import json
from fastapi import HTTPException

from backend.api.routes import (
    create_empty_state,
    build_command_payload,
    build_state_from_payload,
    build_workflow_response,
    require_models,
    workflow_error_response,
    execute_workflow_command,
)
from backend.core.llm.client import WorkflowLLMTimeoutError
from backend.domains.evaluation.registries.metrics import get_metric_by_id
from backend.domains.planning.services.simulation_plan import (
    build_simulation_plan_for_profile_ids,
)
from backend.transport.schemas.workflow import WorkflowCommand
from backend.transport.schemas.workflow import WorkflowStatePayload
from pydantic import TypeAdapter, ValidationError
from tests.fixtures.frontend_mock_data import (
    MOCK_ENVIRONMENT_MODEL,
    MOCK_INTERFACE_MODEL,
    MOCK_TASK_MODEL,
    MOCK_USER_MODEL,
)


def simulation_plan_payload() -> dict:
    metric = get_metric_by_id("cognitive_load")
    assert metric is not None
    return build_simulation_plan_for_profile_ids(
        ["generic"],
        [metric],
    ).model_dump()


def evaluation_metrics_payload() -> dict:
    return {
        "selected_metrics": simulation_plan_payload()["evaluation_metrics"]
    }


def test_create_empty_state_contains_required_keys():
    state = create_empty_state()

    expected_keys = {
        "scenario_description",
        "session_id",
        "current_stage",
        "scenario_context",
        "dimensions",
        "task_model",
        "user_model",
        "user_models",
        "environment_model",
        "computed_parameters",
        "simulation_plan",
        "simulation_model",
        "feedback_target",
        "feedback",
        "revision_instruction",
        "last_feedback",
        "simulation_step",
        "simulation_finished",
        "logs",
        "results",
        "simulation_results",
        "visualization",
    }

    assert expected_keys.issubset(state.keys())


def test_build_state_from_payload_keeps_payload_values():
    payload = {
        "description": "Test scenario",
        "session_id": "abc-123",
        "scenario_context": {"description": "Test scenario"},
        "feedback_target": "task_model",
        "feedback": {"note": "Bitte konkreter"},
        "user_model": {"name": "User Model"},
    }

    state = build_state_from_payload(payload, "review_base_task")

    assert state["scenario_description"] == "Test scenario"
    assert state["session_id"] == "abc-123"
    assert state["current_stage"] == "review_base_task"
    assert state["feedback_target"] == "task_model"
    assert state["feedback"] == {"note": "Bitte konkreter"}
    assert state["user_model"] == {"name": "User Model"}


def test_workflow_state_accepts_profiled_user_models_and_keeps_ids():
    user_models = {
        "generic": {"user_type": "Generic"},
        "adhd": {"user_type": "ADHD"},
    }

    state = build_state_from_payload(
        {
            "description": "Test scenario",
            "user_model": user_models["generic"],
            "user_models": user_models,
        },
        "user_task_environment_models",
    )
    response = build_workflow_response(state)

    assert state["user_model"] == user_models["generic"]
    assert list(state["user_models"]) == ["generic", "adhd"]
    assert response["user_models"]["adhd"]["user_type"] == "ADHD"


def test_workflow_state_accepts_missing_evaluation_metrics():
    payload = WorkflowStatePayload.model_validate({})

    assert payload.evaluation_metrics is None
    assert payload.simulation_plan is None


def test_workflow_state_accepts_evaluation_metrics_selection():
    selection = {
        "selected_metrics": [
            {
                "metric_id": "cognitive_load",
                "name": "Cognitive Load",
                "description": "Kognitive Belastung.",
                "metric_type": "score",
                "source": "predefined",
            }
        ]
    }

    state = build_state_from_payload(
        {"description": "Test scenario", "evaluation_metrics": selection},
        "dimensions",
    )
    response = build_workflow_response(state)

    assert state["evaluation_metrics"]["selected_metrics"][0]["metric_id"] == (
        "cognitive_load"
    )
    assert response["evaluation_metrics"]["selected_metrics"][0][
        "metric_id"
    ] == "cognitive_load"


def test_workflow_state_accepts_and_returns_simulation_plan():
    plan = {
        "selected_user_profiles": [
            {
                "profile_id": "generic",
                "label": "Generic",
                "is_baseline": True,
            }
        ],
        "evaluation_metrics": [
            {
                "metric_id": "cognitive_load",
                "name": "Cognitive Load",
                "description": "Kognitive Belastung.",
                "metric_type": "score",
                "source": "predefined",
            }
        ],
        "simulation_settings": {
            "time_step_seconds": 1,
            "max_duration_seconds": 300,
        },
    }

    state = build_state_from_payload(
        {"description": "Test scenario", "simulation_plan": plan},
        "dimensions",
    )
    response = build_workflow_response(state)

    assert state["simulation_plan"]["selected_user_profiles"][0][
        "profile_id"
    ] == "generic"
    assert response["simulation_plan"]["simulation_settings"][
        "max_duration_seconds"
    ] == 300


def test_build_workflow_response_contains_frontend_state_fields():
    result = {
        "session_id": "session-1",
        "current_stage": "user_task_environment_models",
        "scenario_description": "Test scenario",
        "scenario_context": {"description": "Test scenario"},
        "user_model": {"name": "User Model"},
        "task_model": {"name": "Task Model"},
        "environment_model": {"name": "Environment Model"},
    }

    response = build_workflow_response(result)

    assert response["session_id"] == "session-1"
    assert response["current_stage"] == "user_task_environment_models"
    assert response["scenario_context"] == {"description": "Test scenario"}
    assert response["user_model"] == {"name": "User Model"}
    assert response["task_model"] == {"name": "Task Model"}
    assert response["environment_model"] == {"name": "Environment Model"}
    assert response["computed_parameters"] == {}
    assert response["simulation_model"] == {}
    assert response["simulation_results"] == {}


def test_workflow_command_payload_is_typed_by_command():
    command = TypeAdapter(WorkflowCommand).validate_python(
        {
            "session_id": "session-1",
            "command": "prepare_simulation",
            "payload": {
                "description": "Test scenario",
                "scenario_context": {"description": "Test scenario"},
                "user_model": {"name": "User Model"},
                "task_model": {"name": "Task Model"},
                "environment_model": {"name": "Environment Model"},
                "evaluation_metrics": evaluation_metrics_payload(),
                "simulation_plan": simulation_plan_payload(),
            },
        }
    )

    payload = build_command_payload(command)

    assert payload["session_id"] == "session-1"
    assert payload["user_model"] == {"name": "User Model"}
    assert payload["task_model"] == {"name": "Task Model"}
    assert payload["environment_model"] == {"name": "Environment Model"}


def test_workflow_command_rejects_missing_required_payload_fields():
    with pytest.raises(ValidationError):
        TypeAdapter(WorkflowCommand).validate_python(
            {
                "session_id": "session-1",
                "command": "prepare_simulation",
                "payload": {
                    "description": "Test scenario",
                    "scenario_context": {"description": "Test scenario"},
                    "user_model": {},
                },
            }
        )


def test_require_models_rejects_missing_workflow_prerequisites():
    with pytest.raises(HTTPException) as exc_info:
        require_models(
            {"user_model": {"name": "User Model"}},
            ("user_model", "task_model", "environment_model"),
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail["missing"] == [
        "task_model",
        "environment_model",
    ]


def test_workflow_error_response_is_json():
    response = workflow_error_response(
        ValueError("noise_level has no numeric value")
    )
    payload = json.loads(response.body)

    assert response.status_code == 500
    assert payload == {
        "status": "error",
        "error_type": "ValueError",
        "message": "noise_level has no numeric value",
    }


def test_workflow_timeout_response_names_failed_step():
    response = workflow_error_response(
        WorkflowLLMTimeoutError("scenario_dimensions", 2)
    )
    payload = json.loads(response.body)

    assert response.status_code == 500
    assert payload["error_type"] == "APITimeoutError"
    assert payload["workflow_step"] == "scenario_dimensions"
    assert "after 2 attempts" in payload["message"]


def test_prepare_simulation_returns_computed_parameters():
    command = TypeAdapter(WorkflowCommand).validate_python(
        {
            "session_id": "prepare-integration-test",
            "command": "prepare_simulation",
            "payload": {
                "description": "Urlaubsantrag testen",
                "scenario_context": {"description": "Urlaubsantrag testen"},
                "user_model": MOCK_USER_MODEL,
                "task_model": MOCK_TASK_MODEL,
                "interface_model": MOCK_INTERFACE_MODEL,
                "environment_model": MOCK_ENVIRONMENT_MODEL,
                "evaluation_metrics": evaluation_metrics_payload(),
                "simulation_plan": simulation_plan_payload(),
            },
        }
    )

    result = execute_workflow_command(command)

    assert result["computed_parameters"]["text_complexity"]["value"] == 30
    assert result["computed_parameters"]["navigation_effort"]["value"] == 29
    assert result["simulation_model"]["time_step_seconds"] == 1
    assert sum(
        result["simulation_model"]["model_weights"]["fatigue"]
    ) == pytest.approx(1.0)
