from typing import Any, Literal, NotRequired, TypedDict


JsonDict = dict[str, Any]
FeedbackTarget = Literal[
    "task_model",
    "interface_model",
    "environment_model",
]


class AnalyzeDimensionsPayload(TypedDict):
    description: str
    scenario_description: str
    scenario_text: NotRequired[str]
    scenario_image: NotRequired[JsonDict]
    task_model: NotRequired[JsonDict]
    evaluation_goal_selection: NotRequired[JsonDict]
    evaluation_metrics: NotRequired[JsonDict]
    simulation_plan: NotRequired[JsonDict]


class AnalyzeScreenshotPayload(TypedDict):
    scenario_image: JsonDict


class GenerateUserTaskEnvironmentModelsPayload(TypedDict):
    description: str
    scenario_description: str
    scenario_context: JsonDict
    dimensions: JsonDict
    task_model: NotRequired[JsonDict]
    evaluation_goal_selection: NotRequired[JsonDict]
    evaluation_metrics: NotRequired[JsonDict]
    simulation_plan: NotRequired[JsonDict]


class ModelsPayload(TypedDict):
    description: str
    scenario_description: str
    scenario_context: JsonDict
    user_model: JsonDict
    user_models: NotRequired[JsonDict]
    task_model: JsonDict
    interface_model: JsonDict
    environment_model: JsonDict
    evaluation_goal_selection: NotRequired[JsonDict]
    evaluation_metrics: NotRequired[JsonDict]
    simulation_plan: NotRequired[JsonDict]


class ReviewUserTaskEnvironmentModelsPayload(ModelsPayload):
    feedback_target: FeedbackTarget
    feedback: JsonDict


class PrepareSimulationPayload(ModelsPayload):
    evaluation_metrics: JsonDict
    simulation_plan: JsonDict


class RunSimulationPayload(PrepareSimulationPayload):
    computed_parameters: JsonDict
    simulation_model: JsonDict


class UpdateScenarioModelPayload(ModelsPayload):
    model_type: str
    updated_values: JsonDict
    computed_parameters: NotRequired[JsonDict]


def _with_simulation_plan(payload: dict, simulation_plan: JsonDict | None) -> dict:
    if simulation_plan is not None:
        payload["simulation_plan"] = simulation_plan
    return payload


def _with_evaluation_metrics(
    payload: dict,
    evaluation_metrics: JsonDict | None,
) -> dict:
    if evaluation_metrics is not None:
        payload["evaluation_metrics"] = evaluation_metrics
    return payload


def _with_evaluation_goal_selection(
    payload: dict,
    evaluation_goal_selection: JsonDict | None,
) -> dict:
    if evaluation_goal_selection is not None:
        payload["evaluation_goal_selection"] = evaluation_goal_selection
    return payload


def build_analyze_dimensions_payload(
    description: str,
    simulation_plan: JsonDict | None = None,
    scenario_image: JsonDict | None = None,
    task_model: JsonDict | None = None,
) -> AnalyzeDimensionsPayload:
    payload = {
        "description": description,
        "scenario_description": description,
        "scenario_text": description,
    }
    if scenario_image is not None:
        payload["scenario_image"] = scenario_image
    if task_model:
        payload["task_model"] = task_model
    return _with_simulation_plan(payload, simulation_plan)


def build_analyze_screenshot_payload(
    scenario_image: JsonDict,
) -> AnalyzeScreenshotPayload:
    return {"scenario_image": scenario_image}


def build_generate_user_task_environment_models_payload(
    description: str,
    scenario_context: JsonDict,
    dimensions: JsonDict,
    task_model: JsonDict | None = None,
    simulation_plan: JsonDict | None = None,
    evaluation_metrics: JsonDict | None = None,
    evaluation_goal_selection: JsonDict | None = None,
) -> GenerateUserTaskEnvironmentModelsPayload:
    payload = _with_simulation_plan(
        {
            "description": description,
            "scenario_description": description,
            "scenario_context": scenario_context,
            "dimensions": dimensions,
        },
        simulation_plan,
    )
    if task_model:
        payload["task_model"] = task_model
    payload = _with_evaluation_goal_selection(
        payload,
        evaluation_goal_selection,
    )
    return _with_evaluation_metrics(payload, evaluation_metrics)


def build_models_payload(
    description: str,
    scenario_context: JsonDict,
    user_model: JsonDict,
    task_model: JsonDict,
    interface_model: JsonDict,
    environment_model: JsonDict,
    simulation_plan: JsonDict | None = None,
    user_models: JsonDict | None = None,
    evaluation_goal_selection: JsonDict | None = None,
) -> ModelsPayload:
    payload = {
            "description": description,
            "scenario_description": description,
            "scenario_context": scenario_context,
            "user_model": user_model,
            "task_model": task_model,
            "interface_model": interface_model,
            "environment_model": environment_model,
        }
    if user_models:
        payload["user_models"] = user_models
    payload = _with_evaluation_goal_selection(
        payload,
        evaluation_goal_selection,
    )
    return _with_simulation_plan(payload, simulation_plan)


def build_review_user_task_environment_models_payload(
    description: str,
    scenario_context: JsonDict,
    user_model: JsonDict,
    task_model: JsonDict,
    interface_model: JsonDict,
    environment_model: JsonDict,
    feedback_target: FeedbackTarget,
    feedback: JsonDict,
    simulation_plan: JsonDict | None = None,
) -> ReviewUserTaskEnvironmentModelsPayload:
    return {
        **build_models_payload(
            description=description,
            scenario_context=scenario_context,
            user_model=user_model,
            task_model=task_model,
            interface_model=interface_model,
            environment_model=environment_model,
            simulation_plan=simulation_plan,
        ),
        "feedback_target": feedback_target,
        "feedback": feedback,
    }


def build_prepare_simulation_payload(
    description: str,
    scenario_context: JsonDict,
    user_model: JsonDict,
    task_model: JsonDict,
    interface_model: JsonDict,
    environment_model: JsonDict,
    evaluation_metrics: JsonDict,
    simulation_plan: JsonDict,
    user_models: JsonDict | None = None,
    evaluation_goal_selection: JsonDict | None = None,
) -> PrepareSimulationPayload:
    return {
        **build_models_payload(
            description=description,
            scenario_context=scenario_context,
            user_model=user_model,
            task_model=task_model,
            interface_model=interface_model,
            environment_model=environment_model,
            simulation_plan=simulation_plan,
            user_models=user_models,
            evaluation_goal_selection=evaluation_goal_selection,
        ),
        "evaluation_metrics": evaluation_metrics,
        "simulation_plan": simulation_plan,
    }


def build_run_simulation_payload(
    description: str,
    scenario_context: JsonDict,
    user_model: JsonDict,
    task_model: JsonDict,
    interface_model: JsonDict,
    environment_model: JsonDict,
    computed_parameters: JsonDict,
    evaluation_metrics: JsonDict,
    simulation_plan: JsonDict,
    simulation_model: JsonDict | None = None,
    user_models: JsonDict | None = None,
    evaluation_goal_selection: JsonDict | None = None,
) -> RunSimulationPayload:
    return {
        **build_prepare_simulation_payload(
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
        "computed_parameters": computed_parameters,
        "simulation_model": simulation_model or {},
    }


def build_update_scenario_model_payload(
    description: str,
    scenario_context: JsonDict,
    user_model: JsonDict,
    task_model: JsonDict,
    interface_model: JsonDict,
    environment_model: JsonDict,
    model_type: str,
    updated_values: JsonDict,
    simulation_plan: JsonDict | None = None,
    user_models: JsonDict | None = None,
    computed_parameters: JsonDict | None = None,
) -> UpdateScenarioModelPayload:
    payload = {
        **build_models_payload(
            description=description,
            scenario_context=scenario_context,
            user_model=user_model,
            task_model=task_model,
            interface_model=interface_model,
            environment_model=environment_model,
            simulation_plan=simulation_plan,
            user_models=user_models,
        ),
        "model_type": model_type,
        "updated_values": updated_values,
    }
    if computed_parameters is not None:
        payload["computed_parameters"] = computed_parameters
    return payload
