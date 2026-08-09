import math
from typing import ClassVar, List

from pydantic import BaseModel, Field, model_validator

from backend.core.logging.workflow_logging import logger
from backend.domains.simulation.weights import normalize_weights


class InitialUserStateSchema(BaseModel):
    """Initiale Zustände der Simulation."""

    attention: float = Field(..., ge=0, le=100)
    fatigue: float = Field(..., ge=0, le=100)


class ResponseRatesSchema(BaseModel):
    """Response-Raten der Zustandsübergänge."""

    attention: float = Field(..., ge=0, le=1)
    fatigue: float = Field(..., ge=0, le=1)


class EventThresholdsSchema(BaseModel):
    """Schwellwerte für das Auslösen von Simulationsevents."""

    high_error_risk: float = Field(..., ge=0, le=100)
    very_high_cognitive_load: float = Field(..., ge=0, le=100)
    very_low_attention: float = Field(..., ge=0, le=100)
    time_pressure_warning: float = Field(15.0, ge=0, le=100)
    rework_error_risk: float = Field(62.0, ge=0, le=100)
    high_inhibition_load: float = Field(65.0, ge=0, le=100)
    task_switching_strain: float = Field(65.0, ge=0, le=100)


class ModelWeightsSchema(BaseModel):
    """
    Gewichtungen der linearen Modelle.

    Für jedes lineare Modell wird festgelegt,
    wie viele Einflussfaktoren vorhanden sind.
    """

    WEIGHT_COUNTS: ClassVar[dict[str, int]] = {
        "text_complexity": 4,
        "navigation_effort": 3,
        "decoding_load": 4,
        "visual_reading_load": 4,
        "dyslexia_reading_load": 4,
        "sustained_attention_load": 4,
        "inhibition_load": 4,
        "attention_switching_load": 4,
        "adhd_interaction_load": 4,
        "reading_speed": 4,
        "attention": 6,
        "fatigue": 5,
        "cognitive_load": 5,
        "error_risk": 4,
        "task_success_score": 3,
        "completion_efficiency": 3,
    }
    LEGACY_WEIGHT_ALIASES: ClassVar[dict[str, str]] = {
        "task_success_probability": "task_success_score",
    }

    text_complexity: List[float] = Field(..., min_length=4, max_length=4)
    navigation_effort: List[float] = Field(..., min_length=3, max_length=3)
    decoding_load: List[float] = Field(..., min_length=4, max_length=4)
    visual_reading_load: List[float] = Field(..., min_length=4, max_length=4)
    dyslexia_reading_load: List[float] = Field(..., min_length=4, max_length=4)
    sustained_attention_load: List[float] = Field(..., min_length=4, max_length=4)
    inhibition_load: List[float] = Field(..., min_length=4, max_length=4)
    attention_switching_load: List[float] = Field(..., min_length=4, max_length=4)
    adhd_interaction_load: List[float] = Field(..., min_length=4, max_length=4)
    reading_speed: List[float] = Field(..., min_length=4, max_length=4)

    attention: List[float] = Field(
        ...,
        min_length=6,
        max_length=6,
        description=(
            "Gewichte in der Reihenfolge Distraction Sensitivity, "
            "Distractions, Time Pressure, Fatigue, "
            "Accessibility Support und Context Stability."
        ),
    )

    fatigue: List[float] = Field(..., min_length=5, max_length=5)
    cognitive_load: List[float] = Field(..., min_length=5, max_length=5)
    error_risk: List[float] = Field(..., min_length=4, max_length=4)
    task_success_score: List[float] = Field(
        ...,
        min_length=3,
        max_length=3,
    )
    completion_efficiency: List[float] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_weight_sets(cls, data):
        """
        Normalisiert alle Gewichtungen vor der eigentlichen Pydantic-Validierung.

        Dadurch werden auch vom LLM erzeugte ungültige Gewichtungen
        automatisch in gültige Gewichte überführt.
        """

        if not isinstance(data, dict):
            return data

        normalized_data = dict(data)
        for legacy_name, canonical_name in cls.LEGACY_WEIGHT_ALIASES.items():
            if (
                canonical_name not in normalized_data
                and legacy_name in normalized_data
            ):
                normalized_data[canonical_name] = normalized_data[legacy_name]
            normalized_data.pop(legacy_name, None)

        for field_name, factor_count in cls.WEIGHT_COUNTS.items():
            original = normalized_data.get(field_name, [])
            normalized = normalize_weights(original, factor_count)

            if original != normalized:
                logger.warning(
                    "NORMALIZE_SIMULATION_WEIGHTS field=%s input=%r normalized=%r",
                    field_name,
                    original,
                    normalized,
                )

            normalized_data[field_name] = normalized

        return normalized_data

    @model_validator(mode="after")
    def validate_weight_sets(self):
        """
        Prüft abschließend, ob alle Gewichtungen eine Summe von 1 besitzen.

        Aufgrund der vorherigen Normalisierung sollte diese Prüfung
        normalerweise immer erfolgreich sein.
        """

        for field_name in type(self).model_fields:
            weights = getattr(self, field_name)

            if not math.isclose(
                sum(weights),
                1.0,
                rel_tol=1e-6,
                abs_tol=1e-6,
            ):
                raise ValueError(f"{field_name} weights must sum to 1")

        return self


class TaskStepModifierSchema(BaseModel):
    """
    Optionale Modifikatoren für einzelne Task-Schritte.

    Damit können bestimmte HTA-/GOMS-Schritte gezielt schwieriger
    oder einfacher simuliert werden.
    """

    step_id: str
    attention_modifier: float = Field(1.0, ge=0, le=2)
    fatigue_modifier: float = Field(1.0, ge=0, le=2)
    reading_speed_modifier: float = Field(1.0, ge=0, le=2)
    reason: str


class SimulationModelSchema(BaseModel):
    """
    Strukturierte Beschreibung der Simulationskonfiguration.

    Das LLM liefert dieses Modell als Eingabe für die eigentliche
    Python-Simulation. Die eigentlichen Berechnungen erfolgen
    anschließend deterministisch im Backend.
    """

    time_step_seconds: int = Field(1, ge=1, le=10)
    enable_task_abandonment: bool = True
    max_step_duration_factor: float = Field(3.0, ge=1.0, le=100.0)

    initial_user_state: InitialUserStateSchema
    response_rates: ResponseRatesSchema
    event_thresholds: EventThresholdsSchema
    model_weights: ModelWeightsSchema

    task_step_modifiers: List[TaskStepModifierSchema] = Field(default_factory=list)

    assumptions: List[str] = Field(default_factory=list)
