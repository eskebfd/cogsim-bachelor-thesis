from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, Field

from backend.domains.evaluation.schemas.evaluation_metrics import (
    EvaluationGoalSelection,
    EvaluationMetricsSelection,
)
from backend.domains.scenario.schemas.multimodal import (
    MultimodalAnalysis,
    ScenarioImageMetadata,
    ScenarioImagePayload,
    ScreenshotTaskAnalysis,
)
from backend.domains.planning.schemas.simulation_plan import SimulationPlanSchema


class WorkflowStatePayload(BaseModel):
    session_id: str = "default_session"
    description: str = ""
    scenario_description: str = ""
    scenario_text: str | None = None
    scenario_image: ScenarioImagePayload | None = None
    scenario_image_metadata: ScenarioImageMetadata | None = None
    multimodal_analysis: MultimodalAnalysis | None = None
    screenshot_task_analysis: ScreenshotTaskAnalysis | None = None
    scenario_context: dict = Field(default_factory=dict)
    dimensions: dict = Field(default_factory=dict)
    task_model: dict = Field(default_factory=dict)
    user_model: dict = Field(default_factory=dict)
    user_models: dict = Field(default_factory=dict)
    interface_model: dict = Field(default_factory=dict)
    environment_model: dict = Field(default_factory=dict)
    computed_parameters: dict = Field(default_factory=dict)
    evaluation_goal_selection: EvaluationGoalSelection | None = None
    evaluation_metrics: EvaluationMetricsSelection | None = None
    simulation_plan: SimulationPlanSchema | None = None
    simulation_model: dict = Field(default_factory=dict)
    feedback_target: str = ""
    feedback: dict = Field(default_factory=dict)
    revision_instruction: str = ""
    last_feedback: dict = Field(default_factory=dict)
    logs: list = Field(default_factory=list)
    results: dict = Field(default_factory=dict)
    simulation_results: dict = Field(default_factory=dict)
    visualization: dict = Field(default_factory=dict)
    simulation_step: int = 0
    simulation_finished: bool = False


class AnalyzeDimensionsPayload(BaseModel):
    description: str
    scenario_description: str = ""
    scenario_text: str | None = None
    scenario_image: ScenarioImagePayload | None = None
    task_model: dict = Field(default_factory=dict)
    evaluation_goal_selection: EvaluationGoalSelection | None = None
    evaluation_metrics: EvaluationMetricsSelection | None = None
    simulation_plan: SimulationPlanSchema | None = None


class AnalyzeScreenshotPayload(BaseModel):
    scenario_image: ScenarioImagePayload


class GenerateBaseModelsPayload(BaseModel):
    description: str
    scenario_description: str = ""
    scenario_context: dict
    dimensions: dict = Field(default_factory=dict)
    task_model: dict = Field(default_factory=dict)
    evaluation_goal_selection: EvaluationGoalSelection | None = None
    evaluation_metrics: EvaluationMetricsSelection | None = None
    simulation_plan: SimulationPlanSchema | None = None


class PrepareSimulationPayload(BaseModel):
    description: str
    scenario_description: str = ""
    scenario_context: dict
    user_model: dict
    user_models: dict = Field(default_factory=dict)
    task_model: dict
    interface_model: dict = Field(default_factory=dict)
    environment_model: dict
    evaluation_goal_selection: EvaluationGoalSelection | None = None
    evaluation_metrics: EvaluationMetricsSelection
    simulation_plan: SimulationPlanSchema


class ReviewBaseModelPayload(BaseModel):
    description: str
    scenario_description: str = ""
    scenario_context: dict
    user_model: dict
    user_models: dict = Field(default_factory=dict)
    task_model: dict
    interface_model: dict = Field(default_factory=dict)
    environment_model: dict
    feedback_target: Literal[
        "task_model",
        "interface_model",
        "environment_model",
    ]
    feedback: dict
    evaluation_goal_selection: EvaluationGoalSelection | None = None
    evaluation_metrics: EvaluationMetricsSelection | None = None
    simulation_plan: SimulationPlanSchema | None = None


class RunSimulationPayload(BaseModel):
    description: str
    scenario_description: str = ""
    scenario_context: dict
    user_model: dict
    user_models: dict = Field(default_factory=dict)
    task_model: dict
    interface_model: dict = Field(default_factory=dict)
    environment_model: dict
    computed_parameters: dict
    simulation_model: dict = Field(default_factory=dict)
    evaluation_goal_selection: EvaluationGoalSelection | None = None
    evaluation_metrics: EvaluationMetricsSelection | None = None
    simulation_plan: SimulationPlanSchema


class UpdateScenarioModelPayload(WorkflowStatePayload):
    model_type: Literal["task", "interface", "environment", "user"]
    updated_values: dict


class AnalyzeDimensionsCommand(BaseModel):
    session_id: str = "default_session"
    command: Literal["analyze_dimensions"]
    payload: AnalyzeDimensionsPayload


class AnalyzeScreenshotCommand(BaseModel):
    session_id: str = "default_session"
    command: Literal["analyze_screenshot"]
    payload: AnalyzeScreenshotPayload


class GenerateBaseModelsCommand(BaseModel):
    session_id: str = "default_session"
    command: Literal["generate_base_models"]
    payload: GenerateBaseModelsPayload


class GenerateTaskFlowCommand(BaseModel):
    session_id: str = "default_session"
    command: Literal["generate_task_flow"]
    payload: GenerateBaseModelsPayload


class PrepareSimulationCommand(BaseModel):
    session_id: str = "default_session"
    command: Literal["prepare_simulation"]
    payload: PrepareSimulationPayload


class ReviewBaseModelCommand(BaseModel):
    session_id: str = "default_session"
    command: Literal["review_base_model"]
    payload: ReviewBaseModelPayload


class RunSimulationCommand(BaseModel):
    session_id: str = "default_session"
    command: Literal["run_simulation"]
    payload: RunSimulationPayload


class UpdateScenarioModelCommand(BaseModel):
    session_id: str = "default_session"
    command: Literal["update_scenario_model"]
    payload: UpdateScenarioModelPayload


WorkflowCommand: TypeAlias = Annotated[
    AnalyzeDimensionsCommand
    | AnalyzeScreenshotCommand
    | GenerateTaskFlowCommand
    | GenerateBaseModelsCommand
    | PrepareSimulationCommand
    | ReviewBaseModelCommand
    | RunSimulationCommand
    | UpdateScenarioModelCommand,
    Field(discriminator="command"),
]


class WorkflowResponse(BaseModel):
    session_id: str = "default_session"
    current_stage: str = ""
    scenario_description: str = ""
    scenario_text: str | None = None
    scenario_image_metadata: ScenarioImageMetadata | None = None
    multimodal_analysis: MultimodalAnalysis | None = None
    screenshot_task_analysis: ScreenshotTaskAnalysis | None = None
    scenario_context: dict = Field(default_factory=dict)
    dimensions: dict = Field(default_factory=dict)
    task_model: dict = Field(default_factory=dict)
    user_model: dict = Field(default_factory=dict)
    user_models: dict = Field(default_factory=dict)
    interface_model: dict = Field(default_factory=dict)
    environment_model: dict = Field(default_factory=dict)
    computed_parameters: dict = Field(default_factory=dict)
    evaluation_goal_selection: EvaluationGoalSelection | None = None
    evaluation_metrics: EvaluationMetricsSelection | None = None
    simulation_plan: SimulationPlanSchema | None = None
    simulation_model: dict = Field(default_factory=dict)
    feedback_target: str = ""
    feedback: dict = Field(default_factory=dict)
    revision_instruction: str = ""
    last_feedback: dict = Field(default_factory=dict)
    simulation_step: int = 0
    simulation_finished: bool = False
    logs: list = Field(default_factory=list)
    results: dict = Field(default_factory=dict)
    simulation_results: dict = Field(default_factory=dict)
    visualization: dict = Field(default_factory=dict)
