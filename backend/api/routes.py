import os
import traceback

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from backend.workflow.graph import build_memory_graph
from backend.transport.schemas.workflow import (
    WorkflowCommand,
    WorkflowResponse,
    WorkflowStatePayload,
)
from backend.core.logging.workflow_logging import log_duration, logger
from backend.domains.scenario.services.model_update import update_scenario_model
from backend.core.llm.client import analyze_screenshot_task_structure

router = APIRouter()

memory_graph = build_memory_graph()


def get_graph_config(session_id: str) -> dict:
    return {
        "configurable": {
            "thread_id": session_id,
        }
    }


def create_empty_state() -> dict:
    return {
        "scenario_description": "",
        "scenario_text": None,
        "scenario_image": None,
        "scenario_image_metadata": None,
        "multimodal_analysis": None,
        "screenshot_task_analysis": None,
        "session_id": "default_session",
        "current_stage": "dimensions",
        "scenario_context": {},
        "dimensions": {},
        "task_model": {},
        "user_model": {},
        "user_models": {},
        "interface_model": {},
        "environment_model": {},
        "computed_parameters": {},
        "evaluation_goal_selection": None,
        "evaluation_metrics": None,
        "simulation_plan": None,
        "simulation_model": {},
        "feedback_target": "",
        "feedback": {},
        "revision_instruction": "",
        "last_feedback": {},
        "simulation_step": 0,
        "simulation_finished": False,
        "logs": [],
        "results": {},
        "simulation_results": {},
        "visualization": {},
    }


def build_state_from_payload(payload: dict, current_stage: str) -> dict:
    workflow_payload = WorkflowStatePayload.model_validate(payload)
    payload_data = workflow_payload.model_dump(
        exclude={"description", "scenario_description"}
    )
    state = create_empty_state()

    state.update(
        {
            **payload_data,
            "scenario_description": (
                workflow_payload.scenario_description
                or workflow_payload.scenario_text
                or workflow_payload.description
            ),
            "scenario_text": (
                workflow_payload.scenario_text
                or workflow_payload.scenario_description
                or workflow_payload.description
            ),
            "current_stage": current_stage,
        }
    )

    return state


def invoke_graph(state: dict) -> dict:
    with log_duration(
        "graph.invoke",
        session_id=state.get("session_id", ""),
        current_stage=state.get("current_stage", ""),
    ):
        return memory_graph.invoke(
            state,
            config=get_graph_config(state["session_id"]),
        )


def build_workflow_response(result: dict) -> dict:
    return WorkflowResponse(
        session_id=result.get("session_id", "default_session"),
        current_stage=result.get("current_stage", ""),
        scenario_description=result.get("scenario_description", ""),
        scenario_text=result.get("scenario_text"),
        scenario_image_metadata=result.get("scenario_image_metadata"),
        multimodal_analysis=result.get("multimodal_analysis"),
        screenshot_task_analysis=result.get("screenshot_task_analysis"),
        scenario_context=result.get("scenario_context", {}),
        dimensions=result.get("dimensions", {}),
        task_model=result.get("task_model", {}),
        user_model=result.get("user_model", {}),
        user_models=result.get("user_models", {}),
        environment_model=result.get("environment_model", {}),
        interface_model=result.get("interface_model", {}),
        computed_parameters=result.get("computed_parameters", {}),
        evaluation_goal_selection=result.get("evaluation_goal_selection"),
        evaluation_metrics=result.get("evaluation_metrics"),
        simulation_plan=result.get("simulation_plan"),
        simulation_model=result.get("simulation_model", {}),
        feedback_target=result.get("feedback_target", ""),
        feedback=result.get("feedback", {}),
        revision_instruction=result.get("revision_instruction", ""),
        last_feedback=result.get("last_feedback", {}),
        simulation_step=result.get("simulation_step", 0),
        simulation_finished=result.get("simulation_finished", False),
        logs=result.get("logs", []),
        results=result.get("results", {}),
        simulation_results=result.get("simulation_results", {}),
        visualization=result.get("visualization", {}),
    ).model_dump()


def build_command_payload(command: WorkflowCommand) -> dict:
    payload = command.payload.model_dump()
    payload["session_id"] = command.session_id
    return payload


def require_models(payload: dict, required_keys: tuple[str, ...]) -> None:
    missing = [key for key in required_keys if not payload.get(key)]

    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Workflow prerequisites are missing.",
                "missing": missing,
            },
        )


def workflow_error_response(exc: Exception) -> JSONResponse:
    status_code = exc.status_code if isinstance(exc, HTTPException) else 500
    detail = exc.detail if isinstance(exc, HTTPException) else str(exc)
    message = (
        detail.get("message", str(detail))
        if isinstance(detail, dict)
        else str(detail)
    )
    error_type = getattr(exc, "error_type", type(exc).__name__)
    content = {
        "status": "error",
        "error_type": error_type,
        "message": message or "Unknown backend error.",
    }
    workflow_step = getattr(exc, "workflow_step", None)
    if workflow_step:
        content["workflow_step"] = workflow_step

    if os.getenv("COGSIM_DEBUG", "").lower() in {"1", "true", "yes"}:
        content["traceback"] = traceback.format_exc()

    logger.exception(
        "WORKFLOW_DISPATCH_ERROR error_type=%s message=%s",
        error_type,
        message,
    )
    return JSONResponse(status_code=status_code, content=content)


@router.post("/workflow/dispatch")
def dispatch_workflow_command(command: WorkflowCommand):
    try:
        return execute_workflow_command(command)
    except Exception as exc:
        return workflow_error_response(exc)


def execute_workflow_command(command: WorkflowCommand):
    with log_duration(
        "workflow.command",
        command=command.command,
        session_id=command.session_id,
    ):
        command_payload = build_command_payload(command)
        logger.info(
            "WORKFLOW_COMMAND_PAYLOAD command=%s payload_keys=%s",
            command.command,
            sorted(command_payload.keys()),
        )

        if command.command == "analyze_dimensions":
            state = build_state_from_payload(command_payload, "dimensions")
            result = invoke_graph(state)

            return build_workflow_response(result)

        if command.command == "analyze_screenshot":
            analysis = analyze_screenshot_task_structure(
                command_payload["scenario_image"]
            )
            return build_workflow_response(
                {
                    **create_empty_state(),
                    "session_id": command.session_id,
                    "current_stage": "scenario_screenshot_analysis",
                    "screenshot_task_analysis": analysis,
                }
            )

        if command.command == "generate_base_models":
            state = build_state_from_payload(
                command_payload,
                "user_task_environment_models",
            )
            result = invoke_graph(state)

            return build_workflow_response(result)

        if command.command == "generate_task_flow":
            state = build_state_from_payload(
                command_payload,
                "task_model",
            )
            result = invoke_graph(state)

            return build_workflow_response(result)

        if command.command == "prepare_simulation":
            require_models(
                command_payload,
                (
                    "user_model",
                    "task_model",
                    "interface_model",
                    "environment_model",
                    "simulation_plan",
                ),
            )

            state = build_state_from_payload(
                command_payload,
                "computed_parameters",
            )
            result = invoke_graph(state)

            return build_workflow_response(result)

        if command.command == "review_base_model":
            feedback_target = command_payload.get("feedback_target", "")
            stage_by_target = {
                "task_model": "review_base_task",
                "interface_model": "review_base_interface",
                "environment_model": "review_base_environment",
            }

            state = build_state_from_payload(
                command_payload,
                stage_by_target.get(feedback_target, "review_base_task"),
            )
            result = invoke_graph(state)

            return build_workflow_response(result)

        if command.command == "run_simulation":
            require_models(
                command_payload,
                (
                    "user_model",
                    "task_model",
                    "interface_model",
                    "environment_model",
                    "computed_parameters",
                    "simulation_plan",
                ),
            )

            state = build_state_from_payload(command_payload, "simulation")
            result = invoke_graph(state)

            return build_workflow_response(result)

        if command.command == "update_scenario_model":
            state = build_state_from_payload(
                command_payload,
                "user_task_environment_models",
            )
            result = update_scenario_model(
                model_type=command_payload.get("model_type", ""),
                updated_values=command_payload.get("updated_values", {}),
                state=state,
            )

            return build_workflow_response(result)

        return build_workflow_response(
            build_state_from_payload(
                command_payload,
                "finished",
            )
        )
