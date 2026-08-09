from typing import Literal

from pydantic import BaseModel, Field


ConfidenceLevel = Literal["low", "medium", "high"]


class AttributeValueSchema(BaseModel):
    value: int = Field(
        ...,
        ge=0,
        le=100,
        description="Numerischer Attributwert auf einer Skala von 0 bis 100.",
    )

    scale_min_description: str = Field(
        ...,
        description="Beschreibung, was ein Wert von 0 für dieses Attribut bedeutet.",
    )

    scale_max_description: str = Field(
        ...,
        description="Beschreibung, was ein Wert von 100 für dieses Attribut bedeutet.",
    )

    explanation: str = Field(
        ...,
        description="Kurze Begründung, warum dieser Wert angenommen wurde.",
    )

    confidence: ConfidenceLevel = Field(
        ...,
        description=(
            "Sicherheit des LLMs bei der Schätzung des Attributwerts. "
            "Unabhängig von Wert und Simulation."
        ),
    )
