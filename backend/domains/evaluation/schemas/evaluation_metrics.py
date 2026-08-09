from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


EvaluationMetricSource = Literal["predefined", "custom", "suggested"]
EvaluationMetricType = Literal[
    "time",
    "count",
    "score",
    "probability",
    "ratio",
    "event",
    "state",
]


class EvaluationMetricsBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvaluationMetricDefinition(EvaluationMetricsBaseModel):
    metric_id: str = Field(
        ...,
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Stabile technische ID der Auswertungsmetrik.",
    )
    name: str = Field(..., min_length=1, description="Lesbarer Metrikname.")
    description: str = Field(
        ...,
        min_length=1,
        description="Kurze fachliche Beschreibung der Auswertungsmetrik.",
    )
    metric_type: EvaluationMetricType = Field(
        ...,
        description="Datentyp beziehungsweise Beobachtungsart der Metrik.",
    )
    source: EvaluationMetricSource = Field(
        ...,
        description="Ursprung der Metrik: vordefiniert, benutzerdefiniert oder vorgeschlagen.",
    )
    analysis_question: str | None = Field(
        None,
        description="Optionale Frage, die mit der Metrik beantwortet werden soll.",
    )
    data_basis: str | None = Field(
        None,
        description="Kurze fachliche Beschreibung der verwendeten Datengrundlage.",
    )
    limitation: str | None = Field(
        None,
        description="Kurze methodische Einschränkung der Metrik.",
    )
    expected_output_range: tuple[float, float] | None = Field(
        None,
        description="Optionaler erwarteter Wertebereich als Minimum und Maximum.",
    )
    higher_is_better: bool | None = Field(
        None,
        description="Optionale Angabe zur bevorzugten Richtung der Metrik.",
    )
    requires_simulation: bool = Field(
        True,
        description="Gibt an, ob die Metrik erst aus einer Simulation berechnet werden kann.",
    )
    related_user_profiles: list[str] = Field(
        default_factory=list,
        description="Optionale Profil-IDs, für die die Metrik besonders relevant ist.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Kurze Schlagwörter für Gruppierung und Filterung.",
    )

    @model_validator(mode="after")
    def validate_expected_output_range(self):
        if self.expected_output_range is not None:
            minimum, maximum = self.expected_output_range
            if minimum > maximum:
                raise ValueError(
                    "expected_output_range minimum must not exceed maximum"
                )
        return self


class EvaluationMetricsSelection(EvaluationMetricsBaseModel):
    selected_metrics: list[EvaluationMetricDefinition] = Field(
        ...,
        min_length=1,
        description="Für den Simulationsplan ausgewählte Auswertungsmetriken.",
    )
    custom_metric_requests: list[str] = Field(
        default_factory=list,
        description="Noch nicht strukturierte Wünsche für benutzerdefinierte Metriken.",
    )
    notes: str | None = Field(
        None,
        description="Optionale Hinweise zur Auswahl oder späteren Auswertung.",
    )


class EvaluationGoalDefinition(EvaluationMetricsBaseModel):
    goal_id: str = Field(
        ...,
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Stabile technische ID des Evaluationsziels.",
    )
    name: str = Field(..., min_length=1, description="Lesbarer Zielname.")
    description: str = Field(
        ...,
        min_length=1,
        description="Fachliche Beschreibung des Evaluationsziels.",
    )
    dimension_ids: list[str] = Field(
        ...,
        min_length=1,
        description="Bewertungsdimensionen, die dieses Ziel konkretisieren.",
    )


class EvaluationDimensionDefinition(EvaluationMetricsBaseModel):
    dimension_id: str = Field(
        ...,
        min_length=1,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Stabile technische ID der Bewertungsdimension.",
    )
    name: str = Field(..., min_length=1, description="Lesbarer Dimensionsname.")
    description: str = Field(
        ...,
        min_length=1,
        description="Fachliche Beschreibung der Bewertungsdimension.",
    )
    criterion: str = Field(
        ...,
        min_length=1,
        description="Bewertungskriterium für günstige oder problematische Ausprägungen.",
    )
    metric_ids: list[str] = Field(
        ...,
        min_length=1,
        description="Ergebnismetriken, mit denen diese Dimension bewertet wird.",
    )


class EvaluationGoalSelection(EvaluationMetricsBaseModel):
    selected_goal_ids: list[str] = Field(
        default_factory=list,
        description="Ausgewählte Evaluationsziele.",
    )
    custom_metric_requests: list[str] = Field(
        default_factory=list,
        description="Noch nicht strukturierte Wünsche für zusätzliche Metriken.",
    )

    @model_validator(mode="after")
    def validate_selection_not_empty(self):
        if not self.selected_goal_ids and not self.custom_metric_requests:
            raise ValueError(
                "At least one evaluation goal or custom metric request is required"
            )
        return self


class ResolvedEvaluationSelection(EvaluationMetricsBaseModel):
    selected_goals: list[EvaluationGoalDefinition] = Field(
        default_factory=list,
        description="Aufgelöste Evaluationsziele.",
    )
    resolved_dimensions: list[EvaluationDimensionDefinition] = Field(
        default_factory=list,
        description="Aus den Zielen abgeleitete Bewertungsdimensionen.",
    )
    selected_metrics: EvaluationMetricsSelection = Field(
        ...,
        description="Aus den Dimensionen abgeleitete bestehende Metrikauswahl.",
    )
    custom_metric_requests: list[str] = Field(
        default_factory=list,
        description="Übernommene freie Metrik- oder Analyseanfragen.",
    )
    notes: list[str] = Field(
        default_factory=list,
        description="Hinweise zur Auflösung und zu methodischen Einschränkungen.",
    )
