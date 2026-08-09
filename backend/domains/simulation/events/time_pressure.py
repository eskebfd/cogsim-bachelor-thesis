from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import ResultMetrics, UserState
from backend.domains.simulation.values import rounded


class TimePressureEvent:
    event_type = "time_pressure_warning"

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        time_limit_seconds = context.get("time_limit_seconds")
        elapsed_seconds = context.get("elapsed_seconds", 0)
        remaining_percentage = 100.0
        if time_limit_seconds and time_limit_seconds > 0:
            remaining_percentage = max(
                0.0,
                (time_limit_seconds - elapsed_seconds) / time_limit_seconds * 100,
            )
        threshold = config.event_thresholds.get("time_pressure_warning", 15.0)
        return {
            "active": time_limit_seconds is not None
            and remaining_percentage <= threshold,
            "value": rounded(remaining_percentage),
            "threshold": threshold,
            "message": "Die verbleibende Bearbeitungszeit wird knapp.",
        }

    def effect(self, *, task_step: dict, config: SimulationConfig) -> dict:
        return {
            "attention_change": -2.0,
            "fatigue_change": 1.0,
            "additional_seconds": 0,
        }
