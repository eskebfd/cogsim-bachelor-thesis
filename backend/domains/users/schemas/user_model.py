from typing import List

from pydantic import BaseModel, Field

from backend.domains.models.schemas.attribute import AttributeValueSchema


def _attribute_default(
    value: int,
    minimum: str,
    maximum: str,
) -> AttributeValueSchema:
    return AttributeValueSchema(
        value=value,
        scale_min_description=minimum,
        scale_max_description=maximum,
        explanation="Kompatibler Standardwert für ältere User-Model-Payloads.",
        confidence="medium",
    )


class UserModelSchema(BaseModel):
    user_type: str = Field(
        ...,
        description="Nutzerprofil als simulationsbezogene Modellannahme.",
    )

    reading_difficulty: AttributeValueSchema = Field(
        ...,
        description="Schwierigkeit beim Lesen und Verarbeiten textlicher Informationen.",
    )

    sublexical_decoding_stability: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            75,
            "Graphem-Phonem-Zuordnung ist sehr instabil",
            "Graphem-Phonem-Zuordnung bleibt sehr stabil",
        ),
        description="Stabilität beim Dekodieren unbekannter Wörter über Graphem-Phonem-Zuordnungen.",
    )

    orthographic_processing_stability: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            75,
            "Orthografische Wortverarbeitung ist sehr instabil",
            "Orthografische Wortverarbeitung bleibt sehr stabil",
        ),
        description="Stabilität bei der Verarbeitung bekannter und orthografisch anspruchsvoller Wortformen.",
    )

    parallel_letter_processing_stability: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            75,
            "Mehrere Buchstaben werden kaum parallel erfasst",
            "Mehrere Buchstaben werden sehr stabil parallel erfasst",
        ),
        description="Stabilität beim parallelen Erfassen mehrerer Buchstaben statt rein buchstabierendem Lesen.",
    )

    attention_stability: AttributeValueSchema = Field(
        ...,
        description="Stabilität der Aufmerksamkeit über mehrere Schritte; höhere Werte bedeuten stabilere Aufmerksamkeit.",
    )

    distraction_sensitivity: AttributeValueSchema = Field(
        ...,
        description="Empfindlichkeit gegenüber Ablenkungen.",
    )

    task_switching_difficulty: AttributeValueSchema = Field(
        ...,
        description="Schwierigkeit beim Wechsel zwischen Aufgaben, Kontexten oder Teilhandlungen.",
    )

    vigilance_stability: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            78,
            "Daueraufmerksamkeit bricht sehr schnell ein",
            "Daueraufmerksamkeit bleibt sehr stabil",
        ),
        description="Stabilität der Daueraufmerksamkeit über längere Bearbeitungsphasen.",
    )

    inhibitory_control: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            78,
            "Unpassende Reaktionen werden kaum gehemmt",
            "Unpassende Reaktionen werden sehr stabil gehemmt",
        ),
        description="Fähigkeit, irrelevante Reize oder vorschnelle Handlungen zu unterdrücken.",
    )

    attention_switching_stability: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            78,
            "Aufmerksamkeitswechsel sind sehr instabil",
            "Aufmerksamkeitswechsel bleiben sehr stabil",
        ),
        description="Stabilität beim kontrollierten Wechsel zwischen Reizen, Schritten oder Kontexten.",
    )

    divided_attention_capacity: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            78,
            "Mehrere Informationsquellen können kaum parallel beachtet werden",
            "Mehrere Informationsquellen können sehr gut parallel beachtet werden",
        ),
        description="Fähigkeit, mehrere relevante Informationsquellen gleichzeitig zu beachten.",
    )

    omission_tendency: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            20,
            "Sehr geringe Tendenz, relevante Hinweise zu übersehen",
            "Sehr hohe Tendenz, relevante Hinweise oder Schritte zu übersehen",
        ),
        description="Modellierte Neigung, relevante Hinweise, Signale oder Zwischenschritte auszulassen.",
    )

    reaction_variability: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            20,
            "Reaktionen sind sehr gleichmäßig",
            "Reaktionen schwanken sehr stark",
        ),
        description="Schwankung der Reaktionsgeschwindigkeit während der Bearbeitung.",
    )

    working_memory_stability: AttributeValueSchema = Field(
        ...,
        description="Stabilität des Arbeitsgedächtnisses während der Interaktion.",
    )

    assumptions: List[str] = Field(
        default_factory=list,
        description="Kurze Annahmen zur Herleitung der Werte.",
    )


class ProfiledUserModelSchema(BaseModel):
    profile_id: str = Field(
        ...,
        min_length=1,
        description="Stabile ID des zugehörigen Nutzerprofils.",
    )
    label: str = Field(..., min_length=1, description="Lesbarer Profilname.")
    is_baseline: bool = Field(
        False,
        description="Kennzeichnet das generische Vergleichsmodell.",
    )
    user_model: UserModelSchema
