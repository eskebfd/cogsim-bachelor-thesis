from pydantic import BaseModel, Field


class SummaryStatusView(BaseModel):
    status_id: str
    label: str
    explanation: str
    severity: str
    icon_id: str
    details: str | None = None


class CompletionTimeView(BaseModel):
    label: str
    value_seconds: float
    value_label: str
    basis_label: str
    goms_basis_seconds: float
    goms_basis_label: str
    deviation_seconds: float
    deviation_label: str
    explanation: str
    icon_id: str


class SummaryItemView(BaseModel):
    item_id: str
    label: str
    value: str
    unit: str | None = None
    interpretation: str
    explanation: str
    icon_id: str
    direction: str | None = None


class ResultSummaryView(BaseModel):
    status: SummaryStatusView
    primary_completion_time: CompletionTimeView
    secondary_items: list[SummaryItemView] = Field(default_factory=list)
    explanation: str


class MetricLegendItemView(BaseModel):
    metric_id: str
    label: str
    description: str
    value_range: str
    unit: str
    preferred_direction: str
    interpretation_ranges: list[str] = Field(default_factory=list)
    influencing_factors: list[str] = Field(default_factory=list)
    related_events: list[str] = Field(default_factory=list)
    design_context: list[str] = Field(default_factory=list)


class EventLegendItemView(BaseModel):
    event_id: str
    label: str
    description: str
    trigger_description: str
    trigger_value: str
    severity: str
    state_changes: list[str] = Field(default_factory=list)
    related_metrics: list[str] = Field(default_factory=list)
    possible_consequences: list[str] = Field(default_factory=list)
    design_context: list[str] = Field(default_factory=list)


class ResultSectionDefinitionView(BaseModel):
    section_id: str
    title: str
    short_explanation: str
    icon_id: str


class ResultPresentationView(BaseModel):
    summary: ResultSummaryView
    sections: dict[str, ResultSectionDefinitionView]
    metric_legend: list[MetricLegendItemView]
    event_legend: list[EventLegendItemView]
