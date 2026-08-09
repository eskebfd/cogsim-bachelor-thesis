from backend.domains.simulation.schemas.types import ResultMetrics


class TaskProgressSlowdownAlgorithm:
    algorithm_id = "progress.slowdown"

    def calculate(
        self,
        *,
        task_step: dict,
        user_state: dict,
        result_metrics: ResultMetrics,
        navigation_effort: float,
        dyslexia_reading_load: float = 0.0,
        adhd_interaction_load: float = 0.0,
    ) -> float:
        attention_penalty = (100 - user_state["attention"]) / 100 * 0.25
        fatigue_penalty = user_state["fatigue"] / 100 * 0.25
        load_penalty = result_metrics["cognitive_load"] / 100 * 0.20
        risk_penalty = result_metrics["error_risk"] / 100 * 0.15

        reading_penalty = 0.0
        if task_step.get("step_type") == "read":
            reading_penalty = (
                max(0.0, 75.0 - user_state["reading_speed"]) / 75.0 * 0.80
            )
            reading_penalty += dyslexia_reading_load / 100 * 0.25

        navigation_penalty = 0.0
        if task_step.get("step_type") in {"navigate", "navigation", "select"}:
            navigation_penalty = navigation_effort / 100 * 0.20

        adhd_penalty = 0.0
        if task_step.get("step_type") in {
            "select",
            "decide",
            "check",
            "navigate",
            "navigation",
            "input",
        }:
            adhd_penalty = adhd_interaction_load / 100 * 0.18

        slowdown_factor = 1 + sum(
            (
                attention_penalty,
                fatigue_penalty,
                load_penalty,
                risk_penalty,
                reading_penalty,
                navigation_penalty,
                adhd_penalty,
            )
        )
        return round(1 / min(max(slowdown_factor, 1.0), 2.5), 4)
