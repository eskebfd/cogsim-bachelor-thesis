from typing import List

from pydantic import BaseModel, Field

from backend.domains.models.schemas.attribute import AttributeValueSchema


class EnvironmentModelSchema(BaseModel):
    noise_level: AttributeValueSchema = Field(
        ...,
        description="Lärmniveau der Nutzungssituation.",
    )

    distractions: AttributeValueSchema = Field(
        ...,
        description="Allgemeine Ablenkungsbelastung durch die Umgebung.",
    )

    time_pressure: AttributeValueSchema = Field(
        ...,
        description="Zeitdruck der Nutzungssituation.",
    )

    context_stability: AttributeValueSchema = Field(
        ...,
        description="Stabilität und Vorhersagbarkeit des Nutzungskontexts.",
    )

    visual_distraction: AttributeValueSchema
    interruption_risk: AttributeValueSchema
    social_pressure: AttributeValueSchema
    device_constraints: AttributeValueSchema
    lighting_quality: AttributeValueSchema
    mobility_context: AttributeValueSchema

    external_interruption_frequency: AttributeValueSchema = Field(
        default_factory=lambda: AttributeValueSchema(
            value=25,
            scale_min_description="Kaum externe Unterbrechungen",
            scale_max_description="Sehr häufige externe Unterbrechungen",
            explanation="Kompatibler Standardwert für ältere Environment-Model-Payloads.",
            confidence="medium",
        ),
        description="Häufigkeit externer Unterbrechungen während der Aufgabe.",
    )

    attention_recovery_support: AttributeValueSchema = Field(
        default_factory=lambda: AttributeValueSchema(
            value=65,
            scale_min_description="Wiedereinstieg nach Ablenkung wird kaum unterstützt",
            scale_max_description="Wiedereinstieg nach Ablenkung wird sehr gut unterstützt",
            explanation="Kompatibler Standardwert für ältere Environment-Model-Payloads.",
            confidence="medium",
        ),
        description="Ausmaß, in dem die Umgebung einen Wiedereinstieg nach Ablenkung erleichtert.",
    )

    assumptions: List[str] = Field(
        default_factory=list,
        description="Kurze Annahmen zur Herleitung der Umgebungswerte.",
    )
