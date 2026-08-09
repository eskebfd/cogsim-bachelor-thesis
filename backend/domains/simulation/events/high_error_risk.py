from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import ResultMetrics, UserState


class HighErrorRiskEvent:
    event_type = "high_error_risk"

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        threshold = config.event_thresholds.get("high_error_risk", 60.0)
        return {
            "active": metrics["error_risk"] >= threshold,
            "value": metrics["error_risk"],
            "threshold": threshold,
            "message": "Das modellierte Fehlerrisiko ist kritisch.",
        }

    def effect(self, *, task_step: dict, config: SimulationConfig) -> dict:
        return {
            "attention_change": -1.0,
            "fatigue_change": 1.0,
            "additional_seconds": 0,
        }
