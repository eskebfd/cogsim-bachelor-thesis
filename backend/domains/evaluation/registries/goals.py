from backend.domains.evaluation.schemas.evaluation_metrics import EvaluationGoalDefinition


_EVALUATION_GOALS = (
    EvaluationGoalDefinition(
        goal_id="efficiency",
        name="Effizienz",
        description=(
            "Bewertet, mit welchem Zeit- und Arbeitsaufwand eine Aufgabe "
            "abgeschlossen werden kann."
        ),
        dimension_ids=[
            "processing_time",
            "completion_efficiency",
            "time_limit_exceedance",
        ],
    ),
    EvaluationGoalDefinition(
        goal_id="effectiveness_and_error_safety",
        name="Effektivität und Fehlersicherheit",
        description=(
            "Bewertet, ob eine Aufgabe erfolgreich und möglichst fehlerarm "
            "abgeschlossen werden kann."
        ),
        dimension_ids=[
            "task_success_score",
            "error_risk",
        ],
    ),
    EvaluationGoalDefinition(
        goal_id="cognitive_demand",
        name="Kognitive Beanspruchung",
        description=(
            "Bewertet, wie stark die Aufgabe die kognitiven Ressourcen eines "
            "Nutzerprofils beansprucht."
        ),
        dimension_ids=[
            "cognitive_load",
            "load_related_error_risk",
        ],
    ),
    EvaluationGoalDefinition(
        goal_id="profile_accessibility",
        name="Zugänglichkeit für unterschiedliche Nutzerprofile",
        description=(
            "Bewertet, ob zwischen den simulierten Nutzerprofilen relevante "
            "Unterschiede bei der Aufgabennutzung auftreten."
        ),
        dimension_ids=[
            "profile_time_differences",
            "profile_success_differences",
            "profile_cognitive_load_differences",
            "profile_error_risk_differences",
        ],
    ),
)

_GOALS_BY_ID = {goal.goal_id: goal for goal in _EVALUATION_GOALS}


def get_evaluation_goals() -> list[EvaluationGoalDefinition]:
    return [goal.model_copy(deep=True) for goal in _EVALUATION_GOALS]


def get_evaluation_goal_by_id(goal_id: str) -> EvaluationGoalDefinition | None:
    goal = _GOALS_BY_ID.get(goal_id)
    return goal.model_copy(deep=True) if goal is not None else None
