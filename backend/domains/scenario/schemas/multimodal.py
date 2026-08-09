from typing import Literal

from pydantic import BaseModel, Field


EvidenceSource = Literal["text", "image", "text_and_image", "assumption"]
SignalConfidence = Literal["low", "medium", "high", "unknown"]


class ScenarioImageMetadata(BaseModel):
    filename: str
    mime_type: str
    size_bytes: int = Field(..., ge=1)
    width: int | None = Field(None, ge=1)
    height: int | None = Field(None, ge=1)


class ScenarioImagePayload(BaseModel):
    filename: str
    mime_type: str
    size_bytes: int = Field(..., ge=1)
    data_base64: str = Field(..., min_length=1)


class VisualSignal(BaseModel):
    value: int | None = Field(
        None,
        ge=0,
        le=100,
        description="Geschätzter Wert nur, wenn visuell hinreichend begründbar.",
    )
    confidence: SignalConfidence = "unknown"
    evidence_text: str = ""
    uncertainty_notes: list[str] = Field(default_factory=list)


class ScenarioImageAnalysis(BaseModel):
    text_signals: list[str] = Field(default_factory=list)
    image_signals: list[str] = Field(default_factory=list)
    confirmed_signals: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    confidence_notes: list[str] = Field(default_factory=list)
    interface_signals: dict[str, VisualSignal] = Field(default_factory=dict)
    task_signals: dict[str, VisualSignal] = Field(default_factory=dict)


class ScreenshotHTAStep(BaseModel):
    number: str
    title: str
    description: str = ""
    subtasks: list[str] = Field(default_factory=list)
    interface_elements: list[str] = Field(default_factory=list)
    confidence: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="Sicherheit der aus dem Screenshot abgeleiteten Hypothese.",
    )


class ScreenshotTaskAnalysis(BaseModel):
    user_goal: str = ""
    main_task: str = ""
    task_description: str = ""
    interface_description: str = ""
    hta_steps: list[ScreenshotHTAStep] = Field(default_factory=list)
    decision_points: list[str] = Field(default_factory=list)
    interface_elements: list[str] = Field(default_factory=list)
    visible_elements: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    warning: str | None = None


class MultimodalAnalysis(BaseModel):
    text_signals: list[str] = Field(default_factory=list)
    image_signals: list[str] = Field(default_factory=list)
    confirmed_signals: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    confidence_notes: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    image_analysis_failed: bool = False
    image_analysis_warning: str | None = None
