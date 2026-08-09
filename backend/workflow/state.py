from typing import Any, Literal, NotRequired, TypedDict


JsonDict = dict[str, Any]
WorkflowStage = Literal[
    "dimensions",
    "user_task_environment_models",
    "base_models",
    "task_model",
    "interface_model",
    "environment_model",
    "computed_parameters",
    "review_base_task",
    "review_base_interface",
    "review_base_environment",
    "simulation",
    "finished",
]
FeedbackTarget = Literal[
    "",
    "task_model",
    "interface_model",
    "environment_model",
]


class CogSimState(TypedDict):

    scenario_description: str
    scenario_text: NotRequired[str]
    scenario_image: NotRequired[JsonDict]
    scenario_image_metadata: NotRequired[JsonDict]
    multimodal_analysis: NotRequired[JsonDict]


    session_id: str


    current_stage: WorkflowStage


    scenario_context: JsonDict


    dimensions: JsonDict
    dimension_context: NotRequired[JsonDict]
    task_dimension_signals: NotRequired[JsonDict]
    interface_dimension_signals: NotRequired[JsonDict]
    environment_dimension_signals: NotRequired[JsonDict]


    task_model: JsonDict
    user_model: JsonDict
    user_models: NotRequired[JsonDict]
    interface_model: JsonDict
    environment_model: JsonDict

    computed_parameters: JsonDict
    evaluation_goal_selection: NotRequired[JsonDict]
    evaluation_metrics: NotRequired[JsonDict]
    simulation_plan: NotRequired[JsonDict]
    simulation_model: JsonDict


    feedback_target: FeedbackTarget
    feedback: JsonDict
    revision_instruction: str
    last_feedback: JsonDict


    simulation_step: int
    simulation_finished: bool


    logs: list[JsonDict]
    results: JsonDict
    simulation_results: NotRequired[JsonDict]


    visualization: JsonDict
