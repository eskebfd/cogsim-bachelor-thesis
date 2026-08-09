from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import ResultMetrics, UserState


class TaskAbortedEvent:
    event_type = "task_aborted"

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        max_step_duration = context.get("max_step_duration")
        elapsed_step_seconds = context.get("elapsed_step_seconds", 0)
        task_aborted = (
            context.get("abandonment_enabled", False)
            and context.get("abandonment_allowed", False)
            and max_step_duration is not None
            and elapsed_step_seconds >= max_step_duration
        )
        return {
            "active": task_aborted,
            "value": elapsed_step_seconds,
            "threshold": max_step_duration or 0.0,
            "message": "Maximum step duration exceeded.",
        }

    def effect(self, *, task_step: dict, config: SimulationConfig) -> dict:
        return {
            "attention_change": 0.0,
            "fatigue_change": 0.0,
            "additional_seconds": 0,
        }
