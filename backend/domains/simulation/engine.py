import math
from copy import deepcopy
from collections.abc import Mapping

import backend.domains.simulation.algorithms
from backend.domains.simulation.algorithms.registry import calculate_with_algorithm
from backend.domains.simulation.algorithms.computed_parameters import (
    resolve_computed_task_parameters,
)
from backend.domains.simulation.config import (
    DEFAULT_SIMULATION_CONFIG,
    SimulationConfig,
)
from backend.domains.simulation.events import (
    active_event_types,
    apply_event_effects,
    evaluate_events,
)
from backend.domains.simulation.algorithms.input_factors import build_input_factors
from backend.domains.simulation.metrics import calculate_result_metrics
from backend.domains.simulation.results import (
    build_profile_simulation_result,
    build_simulation_result,
    build_simulation_results,
)
from backend.domains.simulation.algorithms.simulation_model_config import (
    config_from_simulation_model,
)
from backend.domains.simulation.algorithms.state_updates import (
    initialize_user_state,
    update_reading_speed,
    update_user_state,
)
from backend.domains.simulation.schemas.types import ResultMetrics
from backend.core.logging.workflow_logging import logger
from backend.domains.simulation.values import attribute_value


def format_timestamp(seconds: int) -> str:
    """
    Wandelt eine Zeitangabe in Sekunden in das Format MM:SS bzw. HH:MM:SS um.
    """
    minutes, remaining_seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

    return f"{minutes:02d}:{remaining_seconds:02d}"


def normalized_task_steps(task_model: dict) -> list[dict]:
    """
    Bereitet die Task-Schritte für die Simulation vor.

    Stellt sicher, dass jeder Schritt eine gültige Dauer besitzt und ergänzt
    fehlende Standardwerte.
    """
    normalized_steps = []

    for index, step in enumerate(task_model.get("steps", [])):
        raw_duration = step.get("estimated_duration_seconds")


        try:
            duration_seconds = math.ceil(float(raw_duration))
            if duration_seconds <= 0:
                raise ValueError
        except (TypeError, ValueError):

            duration_seconds = 1
            logger.warning(
                "SIMULATION_DURATION_FALLBACK step_id=%s "
                "estimated_duration_seconds=%r fallback_seconds=1",
                step.get("step_id") or f"step_{index + 1}",
                raw_duration,
            )

        normalized_steps.append(
            {
                "step_id": step.get("step_id") or f"step_{index + 1}",
                "name": step.get("name") or f"Schritt {index + 1}",
                "goal": step.get("goal", ""),
                "step_type": step.get("step_type", "unknown"),
                "description": step.get("description", ""),
                "goms_operations": step.get("goms_operations", []),
                "duration_seconds": duration_seconds,
            }
        )

    return normalized_steps


def calculate_task_progress_rate(
    task_step: dict,
    user_state: dict,
    result_metrics: ResultMetrics,
    navigation_effort: float,
    dyslexia_reading_load: float = 0.0,
    adhd_interaction_load: float = 0.0,
) -> float:
    """Return completed GOMS work units per real simulation second."""
    return calculate_with_algorithm(
        "progress.slowdown",
        task_step=task_step,
        user_state=user_state,
        result_metrics=result_metrics,
        navigation_effort=navigation_effort,
        dyslexia_reading_load=dyslexia_reading_load,
        adhd_interaction_load=adhd_interaction_load,
    )


def run_time_discrete_simulation(
    user_model: dict,
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    computed_task_parameters: dict,
    config: SimulationConfig = DEFAULT_SIMULATION_CONFIG,
    simulation_model: dict | None = None,
) -> dict:
    """
    Führt eine zeitdiskrete Simulation eines Nutzungsszenarios durch.

    Für jeden Zeitschritt werden Nutzerzustände aktualisiert,
    Simulationsmetriken berechnet und Ereignisse protokolliert.
    """


    resolved_config = config_from_simulation_model(simulation_model, config)


    task_steps = normalized_task_steps(task_model)
    parameters = resolve_computed_task_parameters(
        task_model,
        interface_model,
        computed_task_parameters,
        environment_model,
        resolved_config.model_weights,
    )


    initial_user_state = initialize_user_state(user_model, resolved_config)
    input_factors = build_input_factors(
        user_model,
        task_model,
        interface_model,
        environment_model,
        parameters,
    )


    user_state = initial_user_state.copy()
    timeline: list[dict] = []
    final_metrics: ResultMetrics | None = None
    previously_active_events: set[str] = set()
    elapsed_seconds = 0
    simulation_completed = bool(task_steps)
    abort_info: dict[str, str | float | None] = {
        "abort_reason": None,
        "aborted_step_id": None,
        "aborted_step_name": None,
        "allowed_step_duration": None,
        "actual_step_duration": None,
    }
    planned_duration = sum(step["duration_seconds"] for step in task_steps)
    time_pressure = attribute_value(environment_model, "time_pressure")
    time_limit_seconds = resolved_config.max_duration_seconds
    if time_pressure >= 50 and planned_duration:
        pressure_factor = 1.2 - 0.4 * (time_pressure / 100)
        time_limit_seconds = min(
            time_limit_seconds,
            planned_duration * pressure_factor,
        )


    for step_index, task_step in enumerate(task_steps):
        elapsed_in_step = 0
        completed_work = 0.0
        required_work = float(task_step["duration_seconds"])
        rework_applied = False


        max_step_duration = (
            task_step["duration_seconds"]
            * max(1.0, resolved_config.max_step_duration_factor)
        )

        step_modifier = resolved_config.task_step_modifiers.get(
            task_step["step_id"],
            {},
        )


        while completed_work < required_work:
            delta_seconds = resolved_config.time_step_seconds

            elapsed_in_step += delta_seconds
            elapsed_seconds += delta_seconds


            user_state = update_user_state(
                user_state,
                user_model,
                task_model,
                interface_model,
                environment_model,
                parameters,
                resolved_config,
                time_step_seconds=delta_seconds,
                step_modifier=step_modifier,
            )


            final_metrics = calculate_result_metrics(
                task_model,
                environment_model,
                parameters,
                user_state,
                resolved_config,
            )
            progress_rate = calculate_task_progress_rate(
                task_step,
                user_state,
                final_metrics,
                parameters["navigation_effort"],
                parameters.get("dyslexia_reading_load", 0.0),
                parameters.get("adhd_interaction_load", 0.0),
            )
            completed_work = min(
                required_work,
                completed_work + delta_seconds * progress_rate,
            )


            events = evaluate_events(
                user_state,
                final_metrics,
                resolved_config,
                previously_active_events,
                elapsed_seconds=elapsed_seconds,
                time_limit_seconds=time_limit_seconds,
                task_step=task_step,
                rework_allowed=not rework_applied,
                abandonment_enabled=resolved_config.enable_task_abandonment,
                abandonment_allowed=completed_work < required_work,
                elapsed_step_seconds=elapsed_in_step,
                max_step_duration=max_step_duration,
                computed_task_parameters=parameters,
            )
            task_aborted = any(
                event["event_type"] == "task_aborted"
                for event in events
            )

            user_state, additional_seconds = apply_event_effects(
                user_state,
                events,
                task_step,
                resolved_config,
            )
            if additional_seconds and not rework_applied:
                required_work += additional_seconds
                rework_applied = True
            if events:
                user_state["reading_speed"] = update_reading_speed(
                    user_model,
                    interface_model,
                    environment_model,
                    parameters,
                    resolved_config,
                    user_state["attention"],
                    user_state["fatigue"],
                    float(step_modifier.get("reading_speed_modifier", 1.0)),
                )
                final_metrics = calculate_result_metrics(
                    task_model,
                    environment_model,
                    parameters,
                    user_state,
                    resolved_config,
                )
            if task_aborted and final_metrics is not None:


                final_metrics = {
                    **final_metrics,
                    "task_success_score": 0.0,
                    "completion_efficiency": 0.0,
                }

            previously_active_events = active_event_types(
                user_state,
                final_metrics,
                resolved_config,
                elapsed_seconds=elapsed_seconds,
                time_limit_seconds=time_limit_seconds,
                task_step=task_step,
                rework_allowed=not rework_applied,
                abandonment_enabled=resolved_config.enable_task_abandonment,
                abandonment_allowed=completed_work < required_work,
                elapsed_step_seconds=elapsed_in_step,
                max_step_duration=max_step_duration,
                computed_task_parameters=parameters,
            )
            task_progress = round(completed_work / required_work, 4)
            step_status = (
                "aborted"
                if task_aborted
                else "completed"
                if completed_work >= required_work
                else "in_progress"
            )


            timeline.append(
                {
                    "timestamp": format_timestamp(elapsed_seconds),
                    "timestamp_seconds": elapsed_seconds,
                    "profile": input_factors["user_profile"],
                    "current_task_step_label": (
                        f"Step {step_index + 1} – "
                        f"{task_step.get('description') or task_step['name']}"
                    ),
                    "task_progress": task_progress,
                    "step_status": step_status,
                    "abort_reason": (
                        "maximum_duration_exceeded" if task_aborted else None
                    ),
                    "base_step_duration": task_step["duration_seconds"],
                    "decoding_load": parameters.get("decoding_load", 0.0),
                    "visual_reading_load": parameters.get(
                        "visual_reading_load",
                        0.0,
                    ),
                    "dyslexia_reading_load": parameters.get(
                        "dyslexia_reading_load",
                        0.0,
                    ),
                    "sustained_attention_load": parameters.get(
                        "sustained_attention_load",
                        0.0,
                    ),
                    "inhibition_load": parameters.get("inhibition_load", 0.0),
                    "attention_switching_load": parameters.get(
                        "attention_switching_load",
                        0.0,
                    ),
                    "adhd_interaction_load": parameters.get(
                        "adhd_interaction_load",
                        0.0,
                    ),
                    "actual_step_duration": calculate_with_algorithm(
                        "completion_time.estimated_duration",
                        required_work=required_work,
                        progress_rate=progress_rate,
                    ),
                    "max_step_duration": max_step_duration,
                    "duration_modifier": round(1 / progress_rate, 4),
                    "current_task_step": {
                        **task_step,
                        "step_index": step_index,
                        "status": step_status,
                        "abort_reason": (
                            "maximum_duration_exceeded"
                            if task_aborted
                            else None
                        ),
                        "elapsed_seconds": elapsed_in_step,
                        "actual_duration_seconds": elapsed_in_step,
                        "max_duration_seconds": max_step_duration,
                        "estimated_duration_seconds": task_step["duration_seconds"],
                        "final_progress": task_progress,
                        "planned_duration_seconds": task_step["duration_seconds"],
                        "effective_duration_seconds": calculate_with_algorithm(
                            "completion_time.estimated_duration",
                            required_work=required_work,
                            progress_rate=progress_rate,
                        ),
                        "completed_work_units": round(completed_work, 4),
                        "required_work_units": round(required_work, 4),
                        "task_progress": task_progress,
                        "task_progress_percent": round(
                            completed_work / required_work * 100,
                            2,
                        ),
                        "progress_rate": progress_rate,
                        "slowdown_factor": round(1 / progress_rate, 4),
                        "simulation_modifier": step_modifier,
                    },
                    "input_factors": input_factors.copy(),
                    "reading_speed": user_state["reading_speed"],
                    "attention": user_state["attention"],
                    "fatigue": user_state["fatigue"],
                    "cognitive_load": final_metrics["cognitive_load"],
                    "error_risk": final_metrics["error_risk"],
                    "task_success_score": final_metrics[
                        "task_success_score"
                    ],
                    "completion_efficiency": final_metrics["completion_efficiency"],
                    "events": events,
                }
            )


            if task_aborted:
                simulation_completed = False
                abort_info = {
                    "abort_reason": "maximum_duration_exceeded",
                    "aborted_step_id": task_step["step_id"],
                    "aborted_step_name": task_step["name"],
                    "allowed_step_duration": max_step_duration,
                    "actual_step_duration": elapsed_in_step,
                }
                break

        if not simulation_completed:
            break


    return build_simulation_result(
        timeline=timeline,
        initial_user_state=initial_user_state,
        final_user_state=user_state,
        final_metrics=final_metrics,
        computed_task_parameters=parameters,
        time_step_seconds=resolved_config.time_step_seconds,
        total_task_steps=len(task_steps),
        simulation_model_used=bool(simulation_model),
        completed=simulation_completed,
        time_limit_seconds=time_limit_seconds,
        **abort_info,
    )


def simulate(
    user_model: dict,
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    computed_task_parameters: dict,
    config: SimulationConfig = DEFAULT_SIMULATION_CONFIG,
    simulation_model: dict | None = None,
) -> dict:
    return run_time_discrete_simulation(
        user_model=user_model,
        task_model=task_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=computed_task_parameters,
        config=config,
        simulation_model=simulation_model,
    )


def simulate_many(
    user_models: Mapping[str, dict],
    task_model: dict,
    interface_model: dict,
    environment_model: dict,
    computed_task_parameters: dict,
    config: SimulationConfig = DEFAULT_SIMULATION_CONFIG,
    simulation_model: dict | None = None,
    profile_labels: Mapping[str, str] | None = None,
    baseline_profile_id: str | None = None,
    selected_metric_ids: set[str] | None = None,
) -> dict:
    profile_results = []
    for profile_id, user_model in user_models.items():
        profile_simulation_model = deepcopy(simulation_model or {})
        if profile_simulation_model:
            profile_simulation_model.setdefault("initial_user_state", {})[
                "attention"
            ] = attribute_value(user_model, "attention_stability", 50.0)
        simulation_result = simulate(
            user_model=user_model,
            task_model=task_model,
            interface_model=interface_model,
            environment_model=environment_model,
            computed_task_parameters=computed_task_parameters,
            config=config,
            simulation_model=profile_simulation_model,
        )
        profile_label = (profile_labels or {}).get(profile_id, profile_id)
        for item in simulation_result.get("timeline", []):
            item["profile"] = profile_id
            item["profile_label"] = profile_label
        profile_results.append(
            build_profile_simulation_result(
                profile_id=profile_id,
                profile_label=profile_label,
                user_model=user_model,
                simulation_result=simulation_result,
            )
        )
    return build_simulation_results(
        profile_results,
        baseline_profile_id=baseline_profile_id,
        selected_metric_ids=selected_metric_ids,
    )
