import pytest

from backend.domains.planning.schemas.simulation_plan import (
    SimulationSettings,
    UserProfileSelection,
)
from backend.domains.evaluation.registries.metrics import get_metric_by_id
from backend.domains.planning.services.simulation_plan import (
    build_simulation_plan,
    computation_models_from_plan,
    get_simulation_plan_or_none,
    has_simulation_plan,
    prepare_simulation_plan_from_state,
    required_attribute_ids_from_plan,
    required_model_types_from_plan,
)


def profile(profile_id: str, *, is_baseline: bool = False):
    return UserProfileSelection(
        profile_id=profile_id,
        label=profile_id.upper(),
        is_baseline=is_baseline,
    )


def metric(metric_id: str):
    result = get_metric_by_id(metric_id)
    assert result is not None
    return result


def test_build_simulation_plan_creates_valid_plan():
    plan = build_simulation_plan(
        [profile("generic", is_baseline=True)],
        [metric("cognitive_load")],
    )

    assert plan.selected_user_profiles[0].profile_id == "generic"
    assert plan.evaluation_metrics[0].metric_id == "cognitive_load"
    assert "cognitive_load" in {
        model.output for model in plan.computation_models
    }


def test_multiple_user_profiles_are_preserved():
    plan = build_simulation_plan(
        [profile("generic", is_baseline=True), profile("adhd")],
        [metric("error_risk")],
    )

    assert [item.profile_id for item in plan.selected_user_profiles] == [
        "generic",
        "adhd",
    ]


def test_cognitive_load_infers_required_attributes():
    plan = build_simulation_plan(
        [profile("generic")],
        [metric("cognitive_load")],
    )

    assert {item.attribute_id for item in plan.required_attributes} == {
        "task_complexity",
        "text_complexity",
        "memory_demand",
        "navigation_effort",
        "fatigue",
    }


def test_time_limit_risk_infers_time_attributes():
    plan = build_simulation_plan(
        [profile("generic")],
        [metric("time_limit_risk")],
    )

    assert {item.attribute_id for item in plan.required_attributes} == {
        "estimated_completion_time",
        "time_limit",
    }


def test_required_models_cover_all_model_types_when_needed():
    plan = build_simulation_plan(
        [profile("generic")],
        [metric("cognitive_load")],
    )

    assert [item.model_type for item in plan.required_models] == [
        "user",
        "task",
        "interface",
        "environment",
    ]
    assert plan.required_models[0].instance_scope == "per_profile"


def test_required_models_remain_complete_for_time_only_metric():
    plan = build_simulation_plan(
        [profile("generic")],
        [metric("completion_time")],
    )

    assert [item.model_type for item in plan.required_models] == [
        "user",
        "task",
        "interface",
        "environment",
    ]


def test_unknown_metric_is_rejected_clearly():
    unknown_metric = metric("cognitive_load").model_copy(
        update={"metric_id": "unknown_metric"}
    )

    with pytest.raises(ValueError, match="unknown_metric"):
        build_simulation_plan([profile("generic")], [unknown_metric])


def test_simulation_settings_can_be_overridden():
    settings = SimulationSettings(
        time_step_seconds=2.0,
        max_duration_seconds=900.0,
        event_thresholds={"high_error_risk": 75.0},
    )

    plan = build_simulation_plan(
        [profile("generic")],
        [metric("completion_time")],
        settings,
    )

    assert plan.simulation_settings == settings
    assert plan.simulation_settings.time_step_seconds == 2.0
    assert plan.simulation_settings.max_duration_seconds == 900.0


def test_optional_simulation_plan_state_helpers():
    plan = build_simulation_plan(
        [profile("generic", is_baseline=True)],
        [metric("cognitive_load")],
    )

    assert has_simulation_plan({}) is False
    assert get_simulation_plan_or_none({}) is None
    assert has_simulation_plan({"simulation_plan": plan.model_dump()}) is True
    resolved = get_simulation_plan_or_none(
        {"simulation_plan": plan.model_dump()}
    )
    assert resolved is not None
    assert resolved.selected_user_profiles[0].profile_id == "generic"


def test_prepare_plan_uses_defaults_without_evaluation_metrics():
    plan = prepare_simulation_plan_from_state({})

    assert plan is not None
    assert [profile.profile_id for profile in plan.selected_user_profiles] == [
        "generic"
    ]
    assert plan.selected_user_profiles[0].is_baseline is True
    assert plan.evaluation_metrics


def test_prepare_plan_uses_evaluation_metrics_and_profile_aliases():
    selection = {
        "selected_metrics": [metric("time_limit_risk").model_dump()]
    }

    plan = prepare_simulation_plan_from_state(
        {
            "scenario_context": {"user_profiles": ["Generisch", "ADHS"]},
            "evaluation_metrics": selection,
        }
    )

    assert plan is not None
    assert [profile.profile_id for profile in plan.selected_user_profiles] == [
        "generic",
        "adhd",
    ]
    assert plan.evaluation_metrics[0].metric_id == "time_limit_risk"


def test_plan_is_central_source_for_orchestration_requirements():
    plan = build_simulation_plan(
        [profile("generic")],
        [metric("cognitive_load")],
    )

    assert required_model_types_from_plan(plan, fallback=["legacy"]) == (
        "user",
        "task",
        "interface",
        "environment",
    )
    assert "task_complexity" in required_attribute_ids_from_plan(
        plan,
        fallback=["legacy_attribute"],
    )
    assert "cognitive_load" in {
        model.output for model in computation_models_from_plan(plan)
    }


def test_orchestration_requirements_keep_legacy_fallback_without_plan():
    assert required_model_types_from_plan(None, fallback=["task"]) == (
        "task",
    )
    assert required_attribute_ids_from_plan(
        None,
        fallback=["task_complexity"],
    ) == ("task_complexity",)
    assert computation_models_from_plan(None) == ()
