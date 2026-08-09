import os
import requests

from frontend.shared.services.workflow_payloads import (
    build_analyze_dimensions_payload,
    build_analyze_screenshot_payload,
    build_generate_user_task_environment_models_payload,
    build_prepare_simulation_payload,
    build_run_simulation_payload,
    build_review_user_task_environment_models_payload,
    build_update_scenario_model_payload,
)
from tests.fixtures.frontend_mock_data import (
    MOCK_DIMENSIONS,
    MOCK_BASE_MODEL_PREVIEW,
    MOCK_COMPUTED_PARAMETERS,
    MOCK_SIMULATION_RESULT,
)

USE_MOCK_DATA = os.getenv("COGSIM_USE_MOCK_DATA") == "true"

BASE_URL = "http://127.0.0.1:8000"

WORKFLOW_DISPATCH_URL = f"{BASE_URL}/workflow/dispatch"


def post_json(url: str, payload: dict) -> dict:
    try:
        response = requests.post(url, json=payload, timeout=180)
    except requests.RequestException as exc:
        raise RuntimeError(f"Backend request failed: {exc}") from exc

    response_text = response.text.strip()

    if not response.ok:
        try:
            error_payload = response.json()
        except ValueError:
            error_payload = None

        if isinstance(error_payload, dict):
            message = error_payload.get("message") or error_payload.get("detail")
            error_type = error_payload.get("error_type", "BackendError")
            workflow_step = error_payload.get("workflow_step")
            step_context = (
                f" in workflow step '{workflow_step}'"
                if workflow_step
                else ""
            )
            raise RuntimeError(
                f"Backend error {response.status_code} ({error_type})"
                f"{step_context}: {message}"
            )

        raise RuntimeError(
            f"Backend error {response.status_code}: "
            f"{response_text or 'empty response'}"
        )

    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "Backend returned a non-JSON response: "
            f"{response_text or 'empty response'}"
        ) from exc

    if not isinstance(result, dict):
        raise RuntimeError(
            f"Backend returned JSON with unexpected type: {type(result).__name__}"
        )

    return result


def dispatch_workflow_command(
    command: str,
    payload: dict,
    session_id: str = "default_session",
) -> dict:
    return post_json(
        WORKFLOW_DISPATCH_URL,
        {
            "session_id": session_id,
            "command": command,
            "payload": payload,
        },
    )


def fetch_scenario_dimensions(
    description: str,
    session_id: str = "default_session",
    simulation_plan: dict | None = None,
    scenario_image: dict | None = None,
    task_model: dict | None = None,
) -> dict:
    if USE_MOCK_DATA:
        return MOCK_DIMENSIONS

    payload = build_analyze_dimensions_payload(
        description,
        simulation_plan,
        scenario_image,
        task_model,
    )

    return dispatch_workflow_command(
        command="analyze_dimensions",
        payload=payload,
        session_id=session_id,
    )


def analyze_screenshot_task_structure(
    scenario_image: dict,
    session_id: str = "default_session",
) -> dict:
    return dispatch_workflow_command(
        command="analyze_screenshot",
        payload=build_analyze_screenshot_payload(scenario_image),
        session_id=session_id,
    )


def generate_user_task_environment_models_workflow(
    description: str,
    scenario_context: dict,
    dimensions: dict,
    session_id: str = "default_session",
    simulation_plan: dict | None = None,
    evaluation_metrics: dict | None = None,
    evaluation_goal_selection: dict | None = None,
    task_model: dict | None = None,
) -> dict:
    if USE_MOCK_DATA:
        return {
            "session_id": session_id,
            "current_stage": "user_task_environment_models",
            "scenario_description": description,
            "scenario_context": scenario_context,
            "dimensions": dimensions,
            "user_model": MOCK_BASE_MODEL_PREVIEW.get("user_model", {}),
            "task_model": MOCK_BASE_MODEL_PREVIEW.get("task_model", {}),
            "interface_model": MOCK_BASE_MODEL_PREVIEW.get("interface_model", {}),
            "environment_model": MOCK_BASE_MODEL_PREVIEW.get(
                "environment_model",
                {},
            ),
            "computed_parameters": {},
            "simulation_plan": simulation_plan,
            "evaluation_goal_selection": evaluation_goal_selection,
            "evaluation_metrics": evaluation_metrics,
            "logs": [],
            "results": {},
            "visualization": {},
            "simulation_step": 0,
            "simulation_finished": False,
        }

    return dispatch_workflow_command(
        command="generate_base_models",
        payload=build_generate_user_task_environment_models_payload(
            description=description,
            scenario_context=scenario_context,
            dimensions=dimensions,
            task_model=task_model,
            simulation_plan=simulation_plan,
            evaluation_metrics=evaluation_metrics,
            evaluation_goal_selection=evaluation_goal_selection,
        ),
        session_id=session_id,
    )


def generate_task_flow_workflow(
    description: str,
    scenario_context: dict,
    session_id: str = "default_session",
    simulation_plan: dict | None = None,
    evaluation_metrics: dict | None = None,
    evaluation_goal_selection: dict | None = None,
) -> dict:
    if USE_MOCK_DATA:
        return {
            "session_id": session_id,
            "current_stage": "task_model",
            "scenario_description": description,
            "scenario_context": scenario_context,
            "dimensions": {},
            "user_model": {},
            "user_models": {},
            "task_model": MOCK_BASE_MODEL_PREVIEW.get("task_model", {}),
            "interface_model": {},
            "environment_model": {},
            "computed_parameters": {},
            "simulation_plan": simulation_plan,
            "evaluation_goal_selection": evaluation_goal_selection,
            "evaluation_metrics": evaluation_metrics,
            "logs": [],
            "results": {},
            "visualization": {},
            "simulation_step": 0,
            "simulation_finished": False,
        }

    return dispatch_workflow_command(
        command="generate_task_flow",
        payload=build_generate_user_task_environment_models_payload(
            description=description,
            scenario_context=scenario_context,
            dimensions={},
            simulation_plan=simulation_plan,
            evaluation_metrics=evaluation_metrics,
            evaluation_goal_selection=evaluation_goal_selection,
        ),
        session_id=session_id,
    )


def prepare_simulation_workflow(
    description: str,
    scenario_context: dict,
    user_model: dict,
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    evaluation_metrics: dict,
    simulation_plan: dict,
    user_models: dict | None = None,
    evaluation_goal_selection: dict | None = None,
    session_id: str = "default_session",
) -> dict:
    if USE_MOCK_DATA:
        return {
            "session_id": session_id,
            "current_stage": "computed_parameters",
            "scenario_description": description,
            "scenario_context": scenario_context,
            "user_model": user_model,
            "task_model": task_model,
            "interface_model": interface_model,
            "environment_model": environment_model,
            "computed_parameters": MOCK_COMPUTED_PARAMETERS,
            "simulation_model": {},
            "simulation_plan": simulation_plan,
            "evaluation_goal_selection": evaluation_goal_selection,
            "evaluation_metrics": evaluation_metrics,
            "logs": [],
            "results": {},
            "visualization": {},
            "simulation_step": 0,
            "simulation_finished": False,
        }

    return dispatch_workflow_command(
        command="prepare_simulation",
        payload=build_prepare_simulation_payload(
            description=description,
            scenario_context=scenario_context,
            user_model=user_model,
            task_model=task_model,
            interface_model=interface_model,
            environment_model=environment_model,
            evaluation_metrics=evaluation_metrics,
            simulation_plan=simulation_plan,
            user_models=user_models,
            evaluation_goal_selection=evaluation_goal_selection,
        ),
        session_id=session_id,
    )


def review_base_model(
    description: str,
    scenario_context: dict,
    user_model: dict,
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    feedback_target: str,
    feedback: dict,
    session_id: str = "default_session",
    simulation_plan: dict | None = None,
) -> dict:
    payload = build_review_user_task_environment_models_payload(
        description=description,
        scenario_context=scenario_context,
        user_model=user_model,
        task_model=task_model,
        interface_model=interface_model,
        environment_model=environment_model,
        feedback_target=feedback_target,
        feedback=feedback,
        simulation_plan=simulation_plan,
    )

    return dispatch_workflow_command(
        command="review_base_model",
        payload=payload,
        session_id=session_id,
    )


def run_simulation_from_models(
    description: str,
    scenario_context: dict,
    user_model: dict,
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    computed_parameters: dict,
    evaluation_metrics: dict,
    simulation_plan: dict,
    simulation_model: dict | None = None,
    user_models: dict | None = None,
    evaluation_goal_selection: dict | None = None,
    session_id: str = "default_session",
) -> dict:
    if USE_MOCK_DATA:
        return MOCK_SIMULATION_RESULT

    payload = build_run_simulation_payload(
        description=description,
        scenario_context=scenario_context,
        user_model=user_model,
        task_model=task_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_parameters=computed_parameters,
        evaluation_metrics=evaluation_metrics,
        simulation_model=simulation_model,
        simulation_plan=simulation_plan,
        user_models=user_models,
        evaluation_goal_selection=evaluation_goal_selection,
    )

    return dispatch_workflow_command(
        command="run_simulation",
        payload=payload,
        session_id=session_id,
    )


def update_scenario_model_workflow(
    description: str,
    scenario_context: dict,
    user_model: dict,
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    model_type: str,
    updated_values: dict,
    session_id: str = "default_session",
    simulation_plan: dict | None = None,
    user_models: dict | None = None,
    computed_parameters: dict | None = None,
) -> dict:
    return dispatch_workflow_command(
        command="update_scenario_model",
        payload=build_update_scenario_model_payload(
            description=description,
            scenario_context=scenario_context,
            user_model=user_model,
            task_model=task_model,
            interface_model=interface_model,
            environment_model=environment_model,
            model_type=model_type,
            updated_values=updated_values,
            simulation_plan=simulation_plan,
            user_models=user_models,
            computed_parameters=computed_parameters,
        ),
        session_id=session_id,
    )
