from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import ResultMetrics, UserState


class LowAttentionEvent:
    event_type = "very_low_attention"

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        threshold = config.event_thresholds.get("very_low_attention", 65.0)
        return {
            "active": user_state["attention"] <= threshold,
            "value": user_state["attention"],
            "threshold": threshold,
            "message": "Die modellierte Aufmerksamkeit ist deutlich abgefallen.",
        }

    def effect(self, *, task_step: dict, config: SimulationConfig) -> dict:
        return {
            "attention_change": -2.0,
            "fatigue_change": 0.0,
            "additional_seconds": 0,
        }
