from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.events.abandonment import TaskAbortedEvent
from backend.domains.simulation.events.executive_function_events import (
    HighInhibitionLoadEvent,
    TaskSwitchingStrainEvent,
)
from backend.domains.simulation.events.high_cognitive_load import HighCognitiveLoadEvent
from backend.domains.simulation.events.high_error_risk import HighErrorRiskEvent
from backend.domains.simulation.events.low_attention import LowAttentionEvent
from backend.domains.simulation.events.registry import (
    EVENT_REGISTRY,
    get_event,
    register_event,
)
from backend.domains.simulation.events.rework import ReworkEvent
from backend.domains.simulation.events.time_pressure import TimePressureEvent
from backend.domains.simulation.schemas.types import ResultMetrics, SimulationEvent, UserState
from backend.domains.simulation.values import clamp, rounded


for _event in (
    HighErrorRiskEvent(),
    HighCognitiveLoadEvent(),
    LowAttentionEvent(),
    TimePressureEvent(),
    ReworkEvent(),
    TaskAbortedEvent(),
    HighInhibitionLoadEvent(),
    TaskSwitchingStrainEvent(),
):
    register_event(_event)


def event_conditions(
    user_state: UserState,
    metrics: ResultMetrics,
    config: SimulationConfig,
    *,
    elapsed_seconds: float = 0,
    time_limit_seconds: float | None = None,
    task_step: dict | None = None,
    rework_allowed: bool = True,
    abandonment_enabled: bool = False,
    abandonment_allowed: bool = False,
    elapsed_step_seconds: float = 0,
    max_step_duration: float | None = None,
    computed_task_parameters: dict | None = None,
) -> dict[str, dict]:
    context = {
        "elapsed_seconds": elapsed_seconds,
        "time_limit_seconds": time_limit_seconds,
        "task_step": task_step,
        "rework_allowed": rework_allowed,
        "abandonment_enabled": abandonment_enabled,
        "abandonment_allowed": abandonment_allowed,
        "elapsed_step_seconds": elapsed_step_seconds,
        "max_step_duration": max_step_duration,
        "computed_task_parameters": computed_task_parameters or {},
    }
    return {
        event.event_type: event.condition(
            user_state=user_state,
            metrics=metrics,
            config=config,
            context=context,
        )
        for event in EVENT_REGISTRY.list_events()
    }


def active_event_types(
    user_state: UserState,
    metrics: ResultMetrics,
    config: SimulationConfig,
    **context,
) -> set[str]:
    return {
        event_type
        for event_type, condition in event_conditions(
            user_state, metrics, config, **context
        ).items()
        if condition["active"]
    }


def evaluate_events(
    user_state: UserState,
    metrics: ResultMetrics,
    config: SimulationConfig,
    previously_active: set[str] | None = None,
    **context,
) -> list[SimulationEvent]:
    events: list[SimulationEvent] = []
    previous = previously_active or set()
    for event_type, condition in event_conditions(
        user_state, metrics, config, **context
    ).items():
        if condition["active"] and event_type not in previous:
            events.append(
                {
                    "event_type": event_type,
                    "severity": "high",
                    "value": condition["value"],
                    "threshold": condition["threshold"],
                    "message": condition["message"],
                }
            )
    return events


def apply_event_effects(
    user_state: UserState,
    events: list[SimulationEvent],
    task_step: dict,
    config: SimulationConfig,
) -> tuple[UserState, int]:
    attention_change = 0.0
    fatigue_change = 0.0
    additional_seconds = 0
    for event in events:
        effect = get_event(event["event_type"]).effect(
            task_step=task_step,
            config=config,
        )
        event_attention_change = float(effect["attention_change"])
        event_fatigue_change = float(effect["fatigue_change"])
        event_additional_seconds = int(effect["additional_seconds"])
        attention_change += event_attention_change
        fatigue_change += event_fatigue_change
        additional_seconds += event_additional_seconds
        event["impact"] = {
            "attention_change": event_attention_change,
            "fatigue_change": event_fatigue_change,
            "additional_seconds": event_additional_seconds,
        }

    return (
        {
            "reading_speed": user_state["reading_speed"],
            "attention": rounded(clamp(user_state["attention"] + attention_change)),
            "fatigue": rounded(clamp(user_state["fatigue"] + fatigue_change)),
        },
        additional_seconds,
    )


__all__ = [
    "EVENT_REGISTRY",
    "active_event_types",
    "apply_event_effects",
    "evaluate_events",
    "event_conditions",
]
