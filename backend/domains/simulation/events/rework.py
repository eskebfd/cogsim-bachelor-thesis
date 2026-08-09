from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import ResultMetrics, UserState


class ReworkEvent:
    event_type = "rework_event"

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        task_step = context.get("task_step") or {}
        rework_allowed = context.get("rework_allowed", True)
        step_type = task_step.get("step_type", "")
        rework_step = step_type in {"input", "check", "submit", "select"}
        threshold = config.event_thresholds.get("rework_error_risk", 62.0)
        return {
            "active": rework_allowed
            and rework_step
            and metrics["error_risk"] >= threshold,
            "value": metrics["error_risk"],
            "threshold": threshold,
            "message": "Ein Korrektur- oder Wiederholungsschritt ist plausibel.",
        }

    def effect(self, *, task_step: dict, config: SimulationConfig) -> dict:
        return {
            "attention_change": 0.0,
            "fatigue_change": 1.0,
            "additional_seconds": min(
                config.maximum_rework_seconds,
                max(
                    1,
                    round(task_step["duration_seconds"] * config.rework_duration_ratio),
                ),
            ),
        }
