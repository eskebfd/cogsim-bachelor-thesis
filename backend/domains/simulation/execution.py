from dataclasses import replace

from backend.domains.planning.services.computed_parameters import (
    build_computed_task_parameters,
)
from backend.domains.planning.services.simulation_plan import get_simulation_plan_or_none
from backend.domains.simulation import run_time_discrete_simulation, simulate_many
from backend.domains.simulation.config import DEFAULT_SIMULATION_CONFIG


def initial_simulation_state() -> dict:
    return {
        "simulation_step": 0,
        "simulation_finished": False,
        "logs": [],
        "results": {},
    }


def _selected_metric_ids_from_state(state: dict) -> set[str] | None:
    selection = state.get("evaluation_metrics")
    if selection is None:
        return None
    selected_metrics = (
        selection.get("selected_metrics", [])
        if isinstance(selection, dict)
        else getattr(selection, "selected_metrics", [])
    )
    metric_ids = set()
    for metric in selected_metrics:
        metric_id = (
            metric.get("metric_id")
            if isinstance(metric, dict)
            else getattr(metric, "metric_id", None)
        )
        if metric_id:
            metric_ids.add(str(metric_id))
    return metric_ids


def run_simulation_from_state(state: dict) -> dict:
    simulation_plan = get_simulation_plan_or_none(state)
    simulation_config = DEFAULT_SIMULATION_CONFIG
    if simulation_plan is not None:
        thresholds = dict(DEFAULT_SIMULATION_CONFIG.event_thresholds)
        thresholds.update(simulation_plan.simulation_settings.event_thresholds or {})
        simulation_config = replace(
            DEFAULT_SIMULATION_CONFIG,
            time_step_seconds=int(simulation_plan.simulation_settings.time_step_seconds),
            max_duration_seconds=(
                simulation_plan.simulation_settings.max_duration_seconds
            ),
            event_thresholds=thresholds,
        )

    computed_task_parameters = state.get("computed_parameters", {})
    selected_metric_ids = _selected_metric_ids_from_state(state)
    if (
        simulation_plan is not None
        and state.get("task_model")
        and state.get("interface_model")
    ):
        computed_task_parameters = build_computed_task_parameters(
            state["task_model"],
            state["interface_model"],
            simulation_plan=simulation_plan,
        ).model_dump()

    user_models = state.get("user_models", {})
    simulation_results = {}
    if len(user_models) > 1:
        profile_labels = (
            {
                profile.profile_id: profile.label
                for profile in simulation_plan.selected_user_profiles
            }
            if simulation_plan is not None
            else {}
        )
        baseline_id = (
            next(
                (
                    profile.profile_id
                    for profile in simulation_plan.selected_user_profiles
                    if profile.is_baseline
                ),
                next(iter(user_models)),
            )
            if simulation_plan is not None
            else next(iter(user_models))
        )
        simulation_results = simulate_many(
            user_models=user_models,
            task_model=state.get("task_model", {}),
            interface_model=state.get("interface_model", {}),
            environment_model=state.get("environment_model", {}),
            computed_task_parameters=computed_task_parameters,
            simulation_model=state.get("simulation_model", {}),
            profile_labels=profile_labels,
            baseline_profile_id=baseline_id,
            config=simulation_config,
            selected_metric_ids=selected_metric_ids,
        )
        result = simulation_results["results_by_profile"][baseline_id]
    else:
        result = run_time_discrete_simulation(
            user_model=state.get("user_model", {}),
            task_model=state.get("task_model", {}),
            interface_model=state.get("interface_model", {}),
            environment_model=state.get("environment_model", {}),
            computed_task_parameters=computed_task_parameters,
            simulation_model=state.get("simulation_model", {}),
            config=simulation_config,
        )

    timeline = result["timeline"]
    output = {
        "simulation_step": len(timeline),
        "simulation_finished": True,
        "logs": timeline,
        "results": result,
    }
    if simulation_results:
        output["simulation_results"] = simulation_results
    return output
