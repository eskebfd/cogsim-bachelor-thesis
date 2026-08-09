from pydantic import BaseModel, Field


class StructuredRecommendationView(BaseModel):
    triggering_metric_ids: list[str] = Field(default_factory=list)
    triggering_event_ids: list[str] = Field(default_factory=list)
    affected_task_step_id: str | None = None
    affected_task_step_name: str
    affected_ui_component: str | None = None
    cause: str
    severity: str
    design_principle: str
    general_recommendation: str
    priority: str
    rule_id: str
    deterministic: bool = True


class RecommendationInterpretationContextView(BaseModel):
    interpretation_role: str = "language_generation_only"
    must_not_change: list[str] = Field(default_factory=list)
    structured_recommendation: StructuredRecommendationView


class RecommendationView(BaseModel):
    recommendation_id: str
    profile_id: str
    title: str
    priority: str
    finding: str
    affected_step: str
    reasoning: str
    supported_causes: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)
    expected_effects: list[str] = Field(default_factory=list)
    affected_metrics: list[str] = Field(default_factory=list)
    related_events: list[str] = Field(default_factory=list)
    usability_principles: list[str] = Field(default_factory=list)
    confidence: str
    is_cross_profile: bool = False
    source_rule_ids: list[str] = Field(default_factory=list)
    structured_recommendation: StructuredRecommendationView
    interpretation_context: RecommendationInterpretationContextView | None = None


class PositiveFindingView(BaseModel):
    profile_id: str
    title: str
    finding: str
    evidence: list[str] = Field(default_factory=list)
