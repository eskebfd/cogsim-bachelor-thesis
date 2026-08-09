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
        explanation="Kompatibler Standardwert für ältere Task-Model-Payloads.",
        confidence="medium",
    )


class GOMSOperationEstimateSchema(BaseModel):
    operation: str
    estimated_duration_seconds: float = Field(..., ge=0)
    cognitive_requirement: str = ""


class TaskStepSchema(BaseModel):
    step_id: str = Field(
        ...,
        description="Stabile ID des HTA-Schritts, z. B. step_1.",
    )

    name: str = Field(
        ...,
        description="Kurzer Name des Bearbeitungsschritts.",
    )

    goal: str = Field(
        ...,
        description="Ziel des Schritts innerhalb der Aufgabe.",
    )

    step_type: str = Field(
        ...,
        description="Typ des Schritts, z. B. read, select, input, decide, check oder submit.",
    )

    description: str = Field(
        ...,
        description="Kurze Beschreibung der Handlung.",
    )

    goms_operations: List[str] = Field(
        default_factory=list,
        description="GOMS-orientierte Teiloperationen, z. B. perceive, think, point, click, type.",
    )

    operation_time_estimates: List[GOMSOperationEstimateSchema] = Field(
        default_factory=list,
        description="Zeitschätzung und kognitive Anforderung pro GOMS-Operation.",
    )

    cognitive_requirements: List[str] = Field(
        default_factory=list,
        description="Kognitive Anforderungen dieses HTA-Schritts.",
    )

    estimated_duration_seconds: float = Field(
        ...,
        ge=1,
        description="Geschätzte Bearbeitungsdauer dieses Schritts in Sekunden.",
    )


class TaskModelSchema(BaseModel):
    task_name: str = Field(
        ...,
        description="Name der Aufgabe.",
    )

    task_goal: str = Field(
        ...,
        description="Übergeordnetes Ziel der Aufgabe.",
    )

    task_complexity: AttributeValueSchema = Field(
        ...,
        description="Gesamtkomplexität der Aufgabe.",
    )

    number_of_steps: AttributeValueSchema = Field(
        ...,
        description=(
            "Reale Anzahl der HTA-Hauptschritte, solange der Wert innerhalb "
            "der bestehenden 0-100-Attributgrenzen liegt."
        ),
    )

    reading_demand: AttributeValueSchema = Field(
        ...,
        description="Text- und Leseanforderung der Aufgabe.",
    )

    unfamiliar_word_density: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            20,
            "Kaum unbekannte oder seltene Wörter",
            "Sehr viele unbekannte, seltene oder fachliche Wörter",
        ),
        description="Anteil unbekannter, seltener oder fachlicher Wörter im Aufgabenmaterial.",
    )

    orthographic_irregularity: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            20,
            "Überwiegend einfache und reguläre Wörter",
            "Viele orthografisch anspruchsvolle, irreguläre oder fremdsprachige Wörter",
        ),
        description="Orthografischer Anspruch durch unregelmäßige, fremdsprachige oder schwer ableitbare Wörter.",
    )

    morphological_complexity: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            25,
            "Kaum zusammengesetzte oder abgeleitete Wörter",
            "Viele zusammengesetzte, abgeleitete oder lange Wortformen",
        ),
        description="Komplexität durch lange, zusammengesetzte oder morphologisch abgeleitete Wörter.",
    )

    sustained_attention_demand: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            35,
            "Kaum längere Aufmerksamkeit erforderlich",
            "Sehr lange ununterbrochene Aufmerksamkeit erforderlich",
        ),
        description="Anforderung, Aufmerksamkeit über längere Zeit stabil zu halten.",
    )

    task_switching_demand: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            30,
            "Kaum Wechsel zwischen Schritten oder Kontexten",
            "Sehr viele Wechsel zwischen Schritten, Reizen oder Kontexten",
        ),
        description="Anforderung durch Wechsel zwischen Arbeitsschritten, Informationen oder Kontexten.",
    )

    inhibition_demand: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            25,
            "Kaum irrelevante Reize oder vorschnelle Handlungen zu hemmen",
            "Sehr viele irrelevante Reize oder vorschnelle Handlungen zu hemmen",
        ),
        description="Anforderung, irrelevante Reize oder unpassende Handlungen zu unterdrücken.",
    )

    divided_attention_demand: AttributeValueSchema = Field(
        default_factory=lambda: _attribute_default(
            30,
            "Kaum parallele Informationsquellen zu beachten",
            "Viele parallele Informationsquellen gleichzeitig zu beachten",
        ),
        description="Anforderung, mehrere relevante Informationsquellen gleichzeitig zu beachten.",
    )

    input_demand: AttributeValueSchema = Field(
        ...,
        description="Anforderung durch Eingaben, Auswahlen oder Formularinteraktion.",
    )

    memory_demand: AttributeValueSchema = Field(
        ...,
        description="Anforderung an Kurzzeitgedächtnis, Reihenfolge oder Merken vorheriger Informationen.",
    )

    decision_demand: AttributeValueSchema = Field(
        ...,
        description="Anforderung durch Entscheidungen und Auswahlalternativen.",
    )

    error_criticality: AttributeValueSchema = Field(
        ...,
        description="Bedeutung möglicher Fehler für den Aufgabenabschluss.",
    )

    steps: List[TaskStepSchema] = Field(
        default_factory=list,
        description="HTA-basierte, geordnete Schrittfolge mit GOMS-orientierter Zeitschätzung.",
    )

    assumptions: List[str] = Field(
        default_factory=list,
        description="Kurze Annahmen zur Herleitung der Werte und Schritte.",
    )
