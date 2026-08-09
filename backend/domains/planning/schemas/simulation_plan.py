from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.domains.evaluation.schemas.evaluation_metrics import (
    EvaluationDimensionDefinition,
    EvaluationGoalDefinition,
    EvaluationMetricDefinition,
)


AttributeCategory = Literal[
    "user",
    "task",
    "interface",
    "environment",
    "computed",
    "state",
    "metric",
]
ComputationModelType = Literal[
    "weighted_sum",
    "difference",
    "ratio",
    "threshold",
    "interaction",
]
RequiredModelType = Literal["user", "task", "interface", "environment"]
ModelInstanceScope = Literal["per_profile", "shared"]
ParameterValue = float | str | bool


class SimulationPlanBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserProfileSelection(SimulationPlanBaseModel):
    profile_id: str = Field(
        ...,
        min_length=1,
        description="Stabile ID des ausgewählten Nutzerprofils.",
    )
    label: str = Field(
        ...,
        min_length=1,
        description="Lesbarer Name des Nutzerprofils.",
    )
    is_baseline: bool = Field(
        False,
        description="Kennzeichnet das Profil als Vergleichsbaseline.",
    )


class RequiredModelDefinition(SimulationPlanBaseModel):
    model_type: RequiredModelType = Field(
        ...,
        description="Benötigter fachlicher Modelltyp.",
    )
    instance_scope: ModelInstanceScope = Field(
        "shared",
        description="Legt fest, ob das Modell geteilt oder pro Profil erzeugt wird.",
    )
    required: bool = Field(
        True,
        description="Gibt an, ob das Modell für die Simulation zwingend benötigt wird.",
    )


class RequiredAttribute(SimulationPlanBaseModel):
    attribute_id: str = Field(
        ...,
        min_length=1,
        description="Stabile ID des benötigten Attributs.",
    )
    name: str = Field(..., min_length=1, description="Lesbarer Attributname.")
    category: AttributeCategory = Field(
        ...,
        description="Fachliche Herkunft oder Rolle des Attributs.",
    )
    required_for_metrics: list[str] = Field(
        default_factory=list,
        description="IDs der Metriken, die dieses Attribut benötigen.",
    )
    editable: bool = Field(
        False,
        description="Gibt an, ob der Attributwert vor der Simulation editierbar ist.",
    )


class ComputationModelInstance(SimulationPlanBaseModel):
    model_id: str = Field(
        ...,
        min_length=1,
        description="Stabile ID der Berechnungsmodellinstanz.",
    )
    name: str = Field(..., min_length=1, description="Lesbarer Modellname.")
    model_type: ComputationModelType = Field(
        ...,
        description="Deterministischer Typ des Berechnungsmodells.",
    )
    inputs: list[str] = Field(
        ...,
        min_length=1,
        description="Attribut- oder Modell-IDs der Eingangsgrößen.",
    )
    output: str = Field(
        ...,
        min_length=1,
        description="ID der erzeugten Ausgangsgröße.",
    )
    weights: dict[str, float] | None = Field(
        None,
        description="Optionale deterministische Gewichtungen der Eingangsgrößen.",
    )
    parameters: dict[str, ParameterValue] | None = Field(
        None,
        description="Optionale Parameter der Berechnungsmodellinstanz.",
    )
    interpretation: str | None = Field(
        None,
        description="Optionale fachliche Interpretation der Berechnung.",
    )


class SimulationSettings(SimulationPlanBaseModel):
    time_step_seconds: float = Field(
        1.0,
        gt=0,
        le=60,
        description="Zeitliche Auflösung der Simulation in Sekunden.",
    )
    max_duration_seconds: float = Field(
        ...,
        gt=0,
        description="Maximale Simulationsdauer in Sekunden.",
    )
    event_thresholds: dict[str, float] | None = Field(
        None,
        description="Optionale Event-Schwellwerte der Simulation.",
    )

    @model_validator(mode="after")
    def validate_duration(self):
        if self.max_duration_seconds < self.time_step_seconds:
            raise ValueError(
                "max_duration_seconds must be at least time_step_seconds"
            )
        return self


class SimulationPlanSchema(SimulationPlanBaseModel):
    selected_user_profiles: list[UserProfileSelection] = Field(
        ...,
        min_length=1,
        description="Nutzerprofile, für die später separat simuliert wird.",
    )
    evaluation_metrics: list[EvaluationMetricDefinition] = Field(
        ...,
        min_length=1,
        description="Auswertungsmetriken des Simulationsvorhabens.",
    )
    evaluation_goals: list[EvaluationGoalDefinition] = Field(
        default_factory=list,
        description="Methodische Evaluationsziele, aus denen Metriken abgeleitet wurden.",
    )
    evaluation_dimensions: list[EvaluationDimensionDefinition] = Field(
        default_factory=list,
        description="Bewertungsdimensionen und Kriterien der Metrikherleitung.",
    )
    required_models: list[RequiredModelDefinition] = Field(
        default_factory=list,
        description="Benötigte fachliche Modelle und ihr Instanziierungsumfang.",
    )
    required_attributes: list[RequiredAttribute] = Field(
        default_factory=list,
        description="Attribute, die für Berechnung und Auswertung benötigt werden.",
    )
    computed_parameters: dict[str, float] = Field(
        default_factory=dict,
        description="Bereits deterministisch berechnete Aufgabenparameter.",
    )
    computation_models: list[ComputationModelInstance] = Field(
        default_factory=list,
        description="Deterministische Berechnungsmodelle des Simulationsplans.",
    )
    simulation_settings: SimulationSettings
