from pydantic import BaseModel, Field
from typing import List, Literal

from backend.domains.models.schemas.base import DeviceType, ScenarioScope
from backend.domains.scenario.schemas.multimodal import (
    EvidenceSource,
    MultimodalAnalysis,
    ScenarioImageMetadata,
)


class TaskOptionSchema(BaseModel):
    label: str = Field(
        ...,
        description="Kurzer Name der erkannten oder vorgeschlagenen Aufgabe.",
    )

    description: str = Field(
        ...,
        description="Kurze Erklärung der Aufgabe.",
    )

    begründung: str = Field(
        ...,
        description="Warum diese Aufgabe aus dem Szenario abgeleitet wurde.",
    )


class EnvironmentOptionSchema(BaseModel):
    label: str = Field(
        ...,
        description="Kurzer Name der Umgebungsoption.",
    )

    description: str = Field(
        ...,
        description="Kurze Erklärung der Umgebung.",
    )

    relevante_faktoren: List[str] = Field(
        default_factory=list,
        description="Relevante Umweltfaktoren dieser Option.",
    )


class InterfaceContextSchema(BaseModel):
    interface_typ: str = Field(
        ...,
        description="Art des digitalen Systems oder Interface-Kontexts, z. B. Online-Shop, Formular, App-Bereich.",
    )

    zentrale_ui_elemente: List[str] = Field(
        default_factory=list,
        description="Zentrale UI-Elemente, die im Szenario wahrscheinlich relevant sind.",
    )

    interaktionsumfang: ScenarioScope = Field(
        ...,
        description="Einschätzung des Umfangs der Interaktion.",
    )

    beschreibung: str = Field(
        ...,
        description="Kurze Beschreibung des Interface-Kontexts.",
    )


class ScenarioAttributeSignalSchema(BaseModel):
    id: str
    name: str
    description: str

    value: int = Field(
        ...,
        ge=0,
        le=100,
        description="Vorläufiger Attributwert auf Basis des Szenarios.",
    )

    label: str
    scale_min_description: str
    scale_max_description: str
    rationale: str
    confidence: Literal["low", "medium", "high"]
    source: EvidenceSource = Field(
        "text",
        description="Evidenzquelle des Signals.",
    )
    evidence_text: str | None = Field(
        None,
        description="Kurzer Hinweis auf die konkrete Text- oder Bildevidenz.",
    )
    uncertainty_notes: List[str] = Field(
        default_factory=list,
        description="Hinweise auf Unsicherheit oder begrenzte Beobachtbarkeit.",
    )


class TaskDimensionSignalsSchema(BaseModel):
    task_complexity: ScenarioAttributeSignalSchema
    number_of_steps: ScenarioAttributeSignalSchema
    reading_demand: ScenarioAttributeSignalSchema
    input_demand: ScenarioAttributeSignalSchema
    memory_demand: ScenarioAttributeSignalSchema
    unfamiliar_word_density: ScenarioAttributeSignalSchema
    orthographic_irregularity: ScenarioAttributeSignalSchema
    morphological_complexity: ScenarioAttributeSignalSchema
    sustained_attention_demand: ScenarioAttributeSignalSchema
    task_switching_demand: ScenarioAttributeSignalSchema
    inhibition_demand: ScenarioAttributeSignalSchema
    divided_attention_demand: ScenarioAttributeSignalSchema


class InterfaceDimensionSignalsSchema(BaseModel):
    text_volume: ScenarioAttributeSignalSchema
    sentence_length: ScenarioAttributeSignalSchema
    word_difficulty: ScenarioAttributeSignalSchema
    technical_terms: ScenarioAttributeSignalSchema
    visual_clutter: ScenarioAttributeSignalSchema
    navigation_complexity: ScenarioAttributeSignalSchema
    accessibility_support: ScenarioAttributeSignalSchema
    feedback_quality: ScenarioAttributeSignalSchema
    text_legibility: ScenarioAttributeSignalSchema
    text_density: ScenarioAttributeSignalSchema
    line_tracking_difficulty: ScenarioAttributeSignalSchema
    stimulus_density: ScenarioAttributeSignalSchema
    irrelevant_signal_load: ScenarioAttributeSignalSchema
    feedback_interruptiveness: ScenarioAttributeSignalSchema
    focus_guidance: ScenarioAttributeSignalSchema


class EnvironmentDimensionSignalsSchema(BaseModel):
    noise_level: ScenarioAttributeSignalSchema
    distractions: ScenarioAttributeSignalSchema
    time_pressure: ScenarioAttributeSignalSchema
    context_stability: ScenarioAttributeSignalSchema
    external_interruption_frequency: ScenarioAttributeSignalSchema
    attention_recovery_support: ScenarioAttributeSignalSchema


class ScenarioDimensionContextSchema(BaseModel):
    detected_device: DeviceType = Field(
        ...,
        description="Erkanntes oder ausgewähltes Gerät.",
    )

    scenario_summary: str = Field(
        ...,
        description="Kurze Zusammenfassung des Nutzungsszenarios.",
    )

    primary_task: TaskOptionSchema = Field(
        ...,
        description="Primär erkannte Aufgabe, die am besten zum Szenario passt.",
    )

    interface_context: InterfaceContextSchema = Field(
        ...,
        description="Erkannter Interface- und Interaktionskontext.",
    )

    task_options: List[TaskOptionSchema] = Field(
        ...,
        description="Weitere sinnvolle Aufgabenoptionen.",
    )

    environment_options: List[EnvironmentOptionSchema] = Field(
        ...,
        description="Sinnvolle Umgebungsoptionen.",
    )

    suggested_metrics: List[str] = Field(
        ...,
        description="Erste vorgeschlagene Metriken für die spätere Simulation.",
    )


class ScenarioDimensionsSchema(BaseModel):
    detected_device: DeviceType = Field(
        ...,
        description="Erkanntes oder ausgewähltes Gerät.",
    )

    scenario_summary: str = Field(
        ...,
        description="Kurze Zusammenfassung des Nutzungsszenarios.",
    )

    primary_task: TaskOptionSchema = Field(
        ...,
        description="Primär erkannte Aufgabe, die am besten zum Szenario passt.",
    )

    interface_context: InterfaceContextSchema = Field(
        ...,
        description="Erkannter Interface- und Interaktionskontext.",
    )

    task_options: List[TaskOptionSchema] = Field(
        ...,
        description="Weitere sinnvolle Aufgabenoptionen.",
    )

    environment_options: List[EnvironmentOptionSchema] = Field(
        ...,
        description="Sinnvolle Umgebungsoptionen.",
    )

    suggested_metrics: List[str] = Field(
        ...,
        description="Erste vorgeschlagene Metriken für die spätere Simulation.",
    )

    task_signals: TaskDimensionSignalsSchema = Field(
        ...,
        description="Strukturierte Szenariohinweise für die späteren Task-Attribute.",
    )

    interface_signals: InterfaceDimensionSignalsSchema = Field(
        ...,
        description="Strukturierte Szenariohinweise für die späteren Interface-Attribute.",
    )

    environment_signals: EnvironmentDimensionSignalsSchema = Field(
        ...,
        description="Strukturierte Szenariohinweise für die späteren Environment-Attribute.",
    )

    scenario_image_metadata: ScenarioImageMetadata | None = None
    multimodal_analysis: MultimodalAnalysis | None = None
