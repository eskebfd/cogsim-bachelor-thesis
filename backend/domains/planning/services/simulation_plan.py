from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from backend.domains.evaluation.schemas.evaluation_metrics import (
    EvaluationDimensionDefinition,
    EvaluationGoalDefinition,
    EvaluationGoalSelection,
    EvaluationMetricDefinition,
    EvaluationMetricsSelection,
)
from backend.domains.planning.schemas.simulation_plan import (
    ComputationModelInstance,
    RequiredAttribute,
    RequiredModelDefinition,
    SimulationPlanSchema,
    SimulationSettings,
    UserProfileSelection,
)
from backend.domains.evaluation.registries.metrics import (
    build_default_evaluation_metrics_selection,
    canonical_metric_id,
)
from backend.domains.evaluation.services.metric_selection import (
    resolve_evaluation_goal_selection,
)
from backend.domains.users.services.user_profiles import build_user_profile_selections


@dataclass(frozen=True)
class MetricRequirements:
    attributes: tuple[str, ...]
    models: tuple[str, ...]
    computation_models: tuple[str, ...]


_ATTRIBUTE_DEFINITIONS = {
    "task_complexity": ("Task Complexity", "task", False),
    "text_complexity": ("Text Complexity", "computed", False),
    "decoding_load": ("Decoding Load", "computed", False),
    "visual_reading_load": ("Visual Reading Load", "computed", False),
    "dyslexia_reading_load": ("Dyslexia Reading Load", "computed", False),
    "sustained_attention_load": ("Sustained Attention Load", "computed", False),
    "inhibition_load": ("Inhibition Load", "computed", False),
    "attention_switching_load": ("Attention Switching Load", "computed", False),
    "adhd_interaction_load": ("ADHS Interaction Load", "computed", False),
    "memory_demand": ("Memory Demand", "task", False),
    "navigation_effort": ("Navigation Effort", "computed", False),
    "fatigue": ("Fatigue", "state", False),
    "cognitive_load": ("Cognitive Load", "metric", False),
    "time_pressure": ("Time Pressure", "environment", True),
    "attention": ("Attention", "state", False),
    "reading_speed": ("Reading Speed", "state", False),
    "task_success_score": ("Task Success Score", "metric", False),
    "error_risk": ("Error Risk Score", "metric", False),
    "estimated_completion_time": ("Estimated Completion Time", "task", False),
    "time_limit": ("Time Limit", "task", True),
}

_METRIC_REQUIREMENTS = {
    "cognitive_load": MetricRequirements(
        attributes=(
            "task_complexity",
            "text_complexity",
            "memory_demand",
            "navigation_effort",
            "fatigue",
        ),
        models=("user", "task", "interface", "environment"),
        computation_models=(
            "text_complexity_model",
            "navigation_effort_model",
            "cognitive_load_model",
        ),
    ),
    "error_risk": MetricRequirements(
        attributes=(
            "cognitive_load",
            "fatigue",
            "time_pressure",
            "attention",
            "dyslexia_reading_load",
        ),
        models=("user", "task", "interface", "environment"),
        computation_models=(
            "decoding_load_model",
            "visual_reading_load_model",
            "dyslexia_reading_load_model",
            "error_risk_model",
        ),
    ),
    "completion_efficiency": MetricRequirements(
        attributes=(
            "reading_speed",
            "attention",
            "task_success_score",
            "dyslexia_reading_load",
        ),
        models=("user", "task", "interface", "environment"),
        computation_models=(
            "decoding_load_model",
            "visual_reading_load_model",
            "dyslexia_reading_load_model",
            "completion_efficiency_model",
        ),
    ),
    "task_success_score": MetricRequirements(
        attributes=("error_risk", "cognitive_load", "navigation_effort"),
        models=("user", "task", "interface", "environment"),
        computation_models=(
            "navigation_effort_model",
            "task_success_score_model",
        ),
    ),
    "completion_time": MetricRequirements(
        attributes=("estimated_completion_time",),
        models=("task",),
        computation_models=("completion_time_model",),
    ),
    "time_limit_risk": MetricRequirements(
        attributes=("estimated_completion_time", "time_limit"),
        models=("task",),
        computation_models=("time_limit_risk_model",),
    ),
    "dyslexia_reading_load": MetricRequirements(
        attributes=(
            "decoding_load",
            "visual_reading_load",
            "dyslexia_reading_load",
            "reading_speed",
            "error_risk",
        ),
        models=("user", "task", "interface", "environment"),
        computation_models=(
            "text_complexity_model",
            "decoding_load_model",
            "visual_reading_load_model",
            "dyslexia_reading_load_model",
        ),
    ),
    "adhd_interaction_load": MetricRequirements(
        attributes=(
            "sustained_attention_load",
            "inhibition_load",
            "attention_switching_load",
            "adhd_interaction_load",
            "attention",
            "error_risk",
        ),
        models=("user", "task", "interface", "environment"),
        computation_models=(
            "sustained_attention_load_model",
            "inhibition_load_model",
            "attention_switching_load_model",
            "adhd_interaction_load_model",
        ),
    ),
}

_COMPUTATION_MODELS = {
    "text_complexity_model": ComputationModelInstance(
        model_id="text_complexity_model",
        name="Text Complexity Model",
        model_type="weighted_sum",
        inputs=[
            "text_volume",
            "sentence_length",
            "word_difficulty",
            "technical_terms",
        ],
        output="text_complexity",
        weights={
            "text_volume": 0.25,
            "sentence_length": 0.25,
            "word_difficulty": 0.25,
            "technical_terms": 0.25,
        },
    ),
    "navigation_effort_model": ComputationModelInstance(
        model_id="navigation_effort_model",
        name="Navigation Effort Model",
        model_type="weighted_sum",
        inputs=[
            "number_of_steps",
            "visual_clutter",
            "navigation_complexity",
        ],
        output="navigation_effort",
        weights={
            "number_of_steps": 1 / 3,
            "visual_clutter": 1 / 3,
            "navigation_complexity": 1 / 3,
        },
    ),
    "decoding_load_model": ComputationModelInstance(
        model_id="decoding_load_model",
        name="Decoding Load Model",
        model_type="weighted_sum",
        inputs=[
            "reading_demand",
            "unfamiliar_word_density",
            "orthographic_irregularity",
            "morphological_complexity",
        ],
        output="decoding_load",
        weights={
            "reading_demand": 0.25,
            "unfamiliar_word_density": 0.25,
            "orthographic_irregularity": 0.25,
            "morphological_complexity": 0.25,
        },
    ),
    "visual_reading_load_model": ComputationModelInstance(
        model_id="visual_reading_load_model",
        name="Visual Reading Load Model",
        model_type="weighted_sum",
        inputs=[
            "text_density",
            "line_tracking_difficulty",
            "visual_clutter",
            "inverse_text_legibility",
        ],
        output="visual_reading_load",
        weights={
            "text_density": 0.25,
            "line_tracking_difficulty": 0.25,
            "visual_clutter": 0.25,
            "inverse_text_legibility": 0.25,
        },
    ),
    "dyslexia_reading_load_model": ComputationModelInstance(
        model_id="dyslexia_reading_load_model",
        name="Dyslexia Reading Load Model",
        model_type="weighted_sum",
        inputs=[
            "decoding_load",
            "visual_reading_load",
            "reading_demand",
            "text_complexity",
        ],
        output="dyslexia_reading_load",
        weights={
            "decoding_load": 0.35,
            "visual_reading_load": 0.25,
            "reading_demand": 0.25,
            "text_complexity": 0.15,
        },
    ),
    "sustained_attention_load_model": ComputationModelInstance(
        model_id="sustained_attention_load_model",
        name="Sustained Attention Load Model",
        model_type="weighted_sum",
        inputs=[
            "sustained_attention_demand",
            "time_pressure",
            "task_complexity",
            "distractions",
        ],
        output="sustained_attention_load",
        weights={
            "sustained_attention_demand": 0.35,
            "time_pressure": 0.25,
            "task_complexity": 0.20,
            "distractions": 0.20,
        },
    ),
    "inhibition_load_model": ComputationModelInstance(
        model_id="inhibition_load_model",
        name="Inhibition Load Model",
        model_type="weighted_sum",
        inputs=[
            "inhibition_demand",
            "irrelevant_signal_load",
            "visual_clutter",
            "feedback_interruptiveness",
        ],
        output="inhibition_load",
        weights={
            "inhibition_demand": 0.35,
            "irrelevant_signal_load": 0.30,
            "visual_clutter": 0.20,
            "feedback_interruptiveness": 0.15,
        },
    ),
    "attention_switching_load_model": ComputationModelInstance(
        model_id="attention_switching_load_model",
        name="Attention Switching Load Model",
        model_type="weighted_sum",
        inputs=[
            "task_switching_demand",
            "navigation_complexity",
            "memory_demand",
            "divided_attention_demand",
        ],
        output="attention_switching_load",
        weights={
            "task_switching_demand": 0.35,
            "navigation_complexity": 0.25,
            "memory_demand": 0.20,
            "divided_attention_demand": 0.20,
        },
    ),
    "adhd_interaction_load_model": ComputationModelInstance(
        model_id="adhd_interaction_load_model",
        name="ADHS Interaction Load Model",
        model_type="weighted_sum",
        inputs=[
            "sustained_attention_load",
            "inhibition_load",
            "attention_switching_load",
            "visual_clutter",
        ],
        output="adhd_interaction_load",
        weights={
            "sustained_attention_load": 0.30,
            "inhibition_load": 0.25,
            "attention_switching_load": 0.25,
            "visual_clutter": 0.20,
        },
    ),
    "cognitive_load_model": ComputationModelInstance(
        model_id="cognitive_load_model",
        name="Cognitive Load Model",
        model_type="weighted_sum",
        inputs=[
            "task_complexity",
            "text_complexity",
            "memory_demand",
            "navigation_effort",
            "fatigue",
        ],
        output="cognitive_load",
        weights={
            "task_complexity": 0.2,
            "text_complexity": 0.2,
            "memory_demand": 0.2,
            "navigation_effort": 0.2,
            "fatigue": 0.2,
        },
    ),
    "error_risk_model": ComputationModelInstance(
        model_id="error_risk_model",
        name="Error Risk Score Model",
        model_type="weighted_sum",
        inputs=[
            "cognitive_load",
            "fatigue",
            "time_pressure",
            "attention",
        ],
        output="error_risk",
        weights={
            "cognitive_load": 0.25,
            "fatigue": 0.25,
            "time_pressure": 0.25,
            "attention": 0.25,
        },
        parameters={
            "invert_attention": True,
            "dyslexia_reading_load_effect": 0.15,
        },
    ),
    "completion_efficiency_model": ComputationModelInstance(
        model_id="completion_efficiency_model",
        name="Completion Efficiency Model",
        model_type="weighted_sum",
        inputs=["reading_speed", "attention", "task_success_score"],
        output="completion_efficiency",
        weights={
            "reading_speed": 1 / 3,
            "attention": 1 / 3,
            "task_success_score": 1 / 3,
        },
    ),
    "task_success_score_model": ComputationModelInstance(
        model_id="task_success_score_model",
        name="Task Success Score Model",
        model_type="difference",
        inputs=["error_risk", "cognitive_load", "navigation_effort"],
        output="task_success_score",
        parameters={"baseline": 100.0},
    ),
    "completion_time_model": ComputationModelInstance(
        model_id="completion_time_model",
        name="Completion Time Model",
        model_type="weighted_sum",
        inputs=["estimated_completion_time"],
        output="completion_time",
        weights={"estimated_completion_time": 1.0},
    ),
    "time_limit_risk_model": ComputationModelInstance(
        model_id="time_limit_risk_model",
        name="Time Limit Risk Model",
        model_type="ratio",
        inputs=["estimated_completion_time", "time_limit"],
        output="time_limit_risk",
        parameters={"scale": 100.0, "clamp_output": True},
    ),
}

_DEFAULT_SIMULATION_SETTINGS = SimulationSettings(
    time_step_seconds=1.0,
    max_duration_seconds=300.0,
)

_PROFILE_ID_ALIASES = {
    "generic": "generic",
    "generisch": "generic",
    "adhd": "adhd",
    "adhs": "adhd",
    "dyslexie": "dyslexie",
    "lese-rechtschreib-schwäche": "dyslexie",
    "lese-rechtschreib-schwaeche": "dyslexie",
}


def _requirements_for_metrics(
    evaluation_metrics: Iterable[EvaluationMetricDefinition],
) -> list[tuple[EvaluationMetricDefinition, MetricRequirements]]:
    resolved = []
    unknown_ids = []
    for metric in evaluation_metrics:
        metric_id = canonical_metric_id(metric.metric_id)
        requirements = _METRIC_REQUIREMENTS.get(metric_id)
        if requirements is None:
            unknown_ids.append(metric.metric_id)
        else:
            resolved.append(
                (metric.model_copy(update={"metric_id": metric_id}), requirements)
            )
    if unknown_ids:
        raise ValueError(
            "No Simulation Plan mapping exists for evaluation metric IDs: "
            + ", ".join(unknown_ids)
        )
    return resolved


def build_required_models(
    evaluation_metrics: list[EvaluationMetricDefinition],
) -> list[RequiredModelDefinition]:
    _requirements_for_metrics(evaluation_metrics)
    model_order = ("user", "task", "interface", "environment")
    return [
        RequiredModelDefinition(
            model_type=model_type,
            instance_scope="per_profile" if model_type == "user" else "shared",
        )
        for model_type in model_order
    ]


def infer_required_attributes_for_metrics(
    evaluation_metrics: list[EvaluationMetricDefinition],
) -> list[RequiredAttribute]:
    required_by_metric: dict[str, list[str]] = {}
    for metric, requirements in _requirements_for_metrics(evaluation_metrics):
        for attribute_id in requirements.attributes:
            required_by_metric.setdefault(attribute_id, []).append(metric.metric_id)

    attributes = []
    for attribute_id, metric_ids in required_by_metric.items():
        name, category, editable = _ATTRIBUTE_DEFINITIONS[attribute_id]
        attributes.append(
            RequiredAttribute(
                attribute_id=attribute_id,
                name=name,
                category=category,
                required_for_metrics=metric_ids,
                editable=editable,
            )
        )
    return attributes


def build_computation_models_for_metrics(
    evaluation_metrics: list[EvaluationMetricDefinition],
) -> list[ComputationModelInstance]:
    model_ids = []
    for _, requirements in _requirements_for_metrics(evaluation_metrics):
        for model_id in requirements.computation_models:
            if model_id not in model_ids:
                model_ids.append(model_id)
    return [_COMPUTATION_MODELS[model_id].model_copy(deep=True) for model_id in model_ids]


def build_simulation_plan(
    selected_user_profiles: list[UserProfileSelection],
    evaluation_metrics: list[EvaluationMetricDefinition],
    simulation_settings: SimulationSettings | None = None,
    evaluation_goals: list[EvaluationGoalDefinition] | None = None,
    evaluation_dimensions: list[EvaluationDimensionDefinition] | None = None,
) -> SimulationPlanSchema:
    profiles = [
        UserProfileSelection.model_validate(profile)
        for profile in selected_user_profiles
    ]
    metrics = [
        EvaluationMetricDefinition.model_validate(metric)
        for metric in evaluation_metrics
    ]
    settings = simulation_settings or _DEFAULT_SIMULATION_SETTINGS.model_copy(
        deep=True
    )
    return SimulationPlanSchema(
        selected_user_profiles=profiles,
        evaluation_metrics=metrics,
        evaluation_goals=evaluation_goals or [],
        evaluation_dimensions=evaluation_dimensions or [],
        required_models=build_required_models(metrics),
        required_attributes=infer_required_attributes_for_metrics(metrics),
        computation_models=build_computation_models_for_metrics(metrics),
        simulation_settings=settings,
    )


def build_simulation_plan_for_profile_ids(
    profile_ids: list[str] | None,
    evaluation_metrics: list[EvaluationMetricDefinition],
    simulation_settings: SimulationSettings | None = None,
    evaluation_goals: list[EvaluationGoalDefinition] | None = None,
    evaluation_dimensions: list[EvaluationDimensionDefinition] | None = None,
) -> SimulationPlanSchema:
    return build_simulation_plan(
        selected_user_profiles=build_user_profile_selections(profile_ids),
        evaluation_metrics=evaluation_metrics,
        simulation_settings=simulation_settings,
        evaluation_goals=evaluation_goals,
        evaluation_dimensions=evaluation_dimensions,
    )


def has_simulation_plan(state: Mapping[str, Any]) -> bool:
    return state.get("simulation_plan") is not None


def get_simulation_plan_or_none(
    state: Mapping[str, Any],
) -> SimulationPlanSchema | None:
    value = state.get("simulation_plan")
    if value is None:
        return None
    if isinstance(value, SimulationPlanSchema):
        return value.model_copy(deep=True)
    return SimulationPlanSchema.model_validate(value)


def required_model_types_from_plan(
    simulation_plan: SimulationPlanSchema | None,
    fallback: Iterable[str] = (),
) -> tuple[str, ...]:
    if simulation_plan is None or not simulation_plan.required_models:
        return tuple(fallback)
    return tuple(
        model.model_type
        for model in simulation_plan.required_models
        if model.required
    )


def required_attribute_ids_from_plan(
    simulation_plan: SimulationPlanSchema | None,
    fallback: Iterable[str] = (),
) -> tuple[str, ...]:
    if simulation_plan is None or not simulation_plan.required_attributes:
        return tuple(fallback)
    return tuple(
        attribute.attribute_id
        for attribute in simulation_plan.required_attributes
    )


def computation_models_from_plan(
    simulation_plan: SimulationPlanSchema | None,
) -> tuple[ComputationModelInstance, ...]:
    if simulation_plan is None:
        return ()
    return tuple(
        model.model_copy(deep=True)
        for model in simulation_plan.computation_models
    )


def _profile_ids_from_state(state: Mapping[str, Any]) -> list[str]:
    scenario_context = state.get("scenario_context") or {}
    raw_profiles = scenario_context.get("user_profiles") or []
    if not raw_profiles and scenario_context.get("user_profile"):
        raw_profiles = [scenario_context["user_profile"]]

    profile_ids = []
    for raw_profile in raw_profiles:
        if isinstance(raw_profile, Mapping):
            raw_profile = raw_profile.get("profile_id", "")
        profile_id = _PROFILE_ID_ALIASES.get(str(raw_profile).strip().lower())
        if profile_id and profile_id not in profile_ids:
            profile_ids.append(profile_id)
    return profile_ids or ["generic"]


def prepare_simulation_plan_from_state(
    state: Mapping[str, Any],
) -> SimulationPlanSchema | None:
    existing_plan = get_simulation_plan_or_none(state)
    if existing_plan is not None:
        return existing_plan

    raw_goal_selection = state.get("evaluation_goal_selection")
    if raw_goal_selection is not None:
        goal_selection = EvaluationGoalSelection.model_validate(
            raw_goal_selection
        )
        resolved_selection = resolve_evaluation_goal_selection(goal_selection)
        selection = resolved_selection.selected_metrics
        evaluation_goals = resolved_selection.selected_goals
        evaluation_dimensions = resolved_selection.resolved_dimensions
    elif state.get("evaluation_metrics") is None:
        selection = build_default_evaluation_metrics_selection()
        evaluation_goals = []
        evaluation_dimensions = []
    else:
        selection = EvaluationMetricsSelection.model_validate(
            state.get("evaluation_metrics")
        )
        evaluation_goals = []
        evaluation_dimensions = []

    return build_simulation_plan_for_profile_ids(
        profile_ids=_profile_ids_from_state(state),
        evaluation_metrics=selection.selected_metrics,
        evaluation_goals=evaluation_goals,
        evaluation_dimensions=evaluation_dimensions,
    )
