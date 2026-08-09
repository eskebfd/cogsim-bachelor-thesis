from typing import Any, NotRequired, TypedDict


class UserState(TypedDict):
    """
    Enthält die dynamischen Zustandsgrößen des simulierten Nutzers.
    Diese Werte werden während der Simulation kontinuierlich aktualisiert.
    """

    reading_speed: float
    attention: float
    fatigue: float


class ResultMetrics(TypedDict):
    """
    Enthält die aus dem aktuellen User State berechneten
    Ergebniskennzahlen eines Simulationsschritts.
    """

    cognitive_load: float
    error_risk: float
    task_success_score: float
    completion_efficiency: float
    completion_time: NotRequired[float]
    time_limit_risk: NotRequired[float]
    dyslexia_reading_load: NotRequired[float]
    adhd_interaction_load: NotRequired[float]


class SimulationEvent(TypedDict):
    """
    Beschreibt ein während der Simulation erkanntes Ereignis,
    beispielsweise ein hohes Fehlerrisiko oder eine sehr geringe
    Aufmerksamkeit.
    """

    event_type: str
    severity: str
    value: float
    threshold: float
    message: str
    impact: NotRequired[dict[str, float | int]]


class ProfileSimulationResult(TypedDict):
    profile_id: str
    profile_label: str
    user_model: dict[str, Any]
    final_state: UserState
    metrics: ResultMetrics
    events: list[dict[str, Any]]
    timeline: list[dict[str, Any]]
    problems: list[str]
    recommendations: list[str]
    recommendation_cards: NotRequired[list[dict[str, Any]]]
    positive_findings: NotRequired[list[dict[str, Any]]]
    completed: bool
    status: str
    abort_reason: str | None
    aborted_step_id: str | None
    aborted_step_name: str | None
    allowed_step_duration: float | None
    actual_step_duration: float | None


class MultiProfileSimulationResult(TypedDict):
    completed: bool
    profile_count: int
    profile_ids: list[str]
    baseline_profile_id: str | None
    results_by_profile: dict[str, ProfileSimulationResult]
    runs: list[ProfileSimulationResult]
    comparison_summary: dict[str, Any] | None
    result_presentation: NotRequired[dict[str, Any]]
