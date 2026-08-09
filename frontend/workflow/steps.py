from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowStep:
    number: int
    step_id: str
    label: str
    feature: str
    description: str = ""
    required_state_keys: tuple[str, ...] = ()


USER_PROFILES_STEP = 1
METRICS_STEP = 2
SCENARIO_STEP = 3
TASK_FLOW_STEP = 4
DIMENSIONS_STEP = 5
SIMULATION_FOUNDATIONS_STEP = 6
SIMULATION_PLAN_STEP = 7
RESULTS_STEP = 8


WORKFLOW_STEP_DEFINITIONS = (
    WorkflowStep(
        USER_PROFILES_STEP,
        "user_profiles",
        "Nutzerprofile",
        "user_profiles",
        "Auswahl der zu simulierenden Referenzprofile.",
    ),
    WorkflowStep(
        METRICS_STEP,
        "metrics",
        "Auswertung",
        "evaluation_goals",
        "Auswahl der Kennwerte, die später ausgewertet werden.",
        ("user_profiles",),
    ),
    WorkflowStep(
        SCENARIO_STEP,
        "scenario",
        "Szenario",
        "scenario",
        "Beschreibung von Aufgabe, Interface und Nutzungssituation.",
        ("evaluation_metrics",),
    ),
    WorkflowStep(
        TASK_FLOW_STEP,
        "task_flow",
        "Aufgabenablauf",
        "task_flow",
        "Erzeugung und Prüfung des erkannten Aufgabenablaufs.",
        ("scenario_input",),
    ),
    WorkflowStep(
        DIMENSIONS_STEP,
        "dimensions",
        "Anforderungen",
        "dimensions",
        "Prüfung der automatisch erkannten Szenarioanforderungen.",
        ("base_model_preview",),
    ),
    WorkflowStep(
        SIMULATION_FOUNDATIONS_STEP,
        "simulation_foundations",
        "Simulationsgrundlagen",
        "models",
        "Übersicht der erzeugten Modelle für die spätere Simulation.",
        ("dimensions", "base_model_preview"),
    ),
    WorkflowStep(
        SIMULATION_PLAN_STEP,
        "simulation_plan",
        "Simulationsplan",
        "computed_parameters",
        "Prüfung berechneter Planwerte vor dem Simulationslauf.",
        ("base_model_preview", "computed_parameters_preview"),
    ),
    WorkflowStep(
        RESULTS_STEP,
        "results",
        "Ergebnisse",
        "simulation",
        "Vergleich der Simulationsergebnisse und Empfehlungen.",
        ("simulation_result",),
    ),
)


WORKFLOW_STEPS = [
    (step.number, step.label) for step in WORKFLOW_STEP_DEFINITIONS
]


def workflow_step_by_number(step_number: int) -> WorkflowStep | None:
    return next(
        (
            step
            for step in WORKFLOW_STEP_DEFINITIONS
            if step.number == step_number
        ),
        None,
    )
