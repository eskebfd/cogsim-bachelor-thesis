from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import ResultMetrics, UserState


class HighCognitiveLoadEvent:
    event_type = "very_high_cognitive_load"

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        threshold = config.event_thresholds.get("very_high_cognitive_load", 65.0)
        return {
            "active": metrics["cognitive_load"] >= threshold,
            "value": metrics["cognitive_load"],
            "threshold": threshold,
            "message": "Die modellierte kognitive Belastung ist hoch.",
        }

    def effect(self, *, task_step: dict, config: SimulationConfig) -> dict:
        return {
            "attention_change": 0.0,
            "fatigue_change": 2.0,
            "additional_seconds": 0,
        }
