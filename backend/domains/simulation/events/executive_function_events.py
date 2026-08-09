from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.schemas.types import ResultMetrics, UserState


class HighInhibitionLoadEvent:
    event_type = "high_inhibition_load"

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        parameters = context.get("computed_task_parameters") or {}
        value = float(parameters.get("inhibition_load", 0.0))
        threshold = config.event_thresholds.get("high_inhibition_load", 65.0)

        return {
            "active": value >= threshold,
            "value": value,
            "threshold": threshold,
            "message": (
                "Die Oberfläche oder Aufgabe verlangt hohe Hemmung "
                "irrelevanter Reize."
            ),
        }

    def effect(self, *, task_step: dict, config: SimulationConfig) -> dict:
        return {
            "attention_change": -0.5,
            "fatigue_change": 0.5,
            "additional_seconds": 0,
        }


class TaskSwitchingStrainEvent:
    event_type = "task_switching_strain"

    def condition(
        self,
        *,
        user_state: UserState,
        metrics: ResultMetrics,
        config: SimulationConfig,
        context: dict,
    ) -> dict:
        task_step = context.get("task_step") or {}
        parameters = context.get("computed_task_parameters") or {}
        value = float(parameters.get("attention_switching_load", 0.0))
        threshold = config.event_thresholds.get("task_switching_strain", 65.0)
        switching_step = task_step.get("step_type") in {
            "select",
            "decide",
            "check",
            "navigate",
            "navigation",
        }

        return {
            "active": switching_step and value >= threshold,
            "value": value,
            "threshold": threshold,
            "message": (
                "Der Schritt verlangt belastende Wechsel zwischen Informationen "
                "oder Handlungsoptionen."
            ),
        }

    def effect(self, *, task_step: dict, config: SimulationConfig) -> dict:
        return {
            "attention_change": -0.5,
            "fatigue_change": 0.75,
            "additional_seconds": 0,
        }
