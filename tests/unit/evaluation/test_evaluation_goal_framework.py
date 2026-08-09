import pytest

from backend.domains.evaluation.services.metric_selection import (
    get_evaluation_dimensions,
    get_evaluation_goals,
    resolve_evaluation_goal_selection,
)
from backend.domains.evaluation.schemas.evaluation_metrics import EvaluationGoalSelection
from backend.domains.evaluation.registries.metrics import (
    get_metric_by_id,
    get_predefined_evaluation_metrics,
)
from backend.domains.planning.services.simulation_plan import (
    prepare_simulation_plan_from_state,
)
from frontend.features.evaluation_goals.section import (
    build_evaluation_goal_selection,
    build_evaluation_selection_bundle,
    build_metric_selection_bundle,
    _metric_display_content,
)
from frontend.shared.services.workflow_payloads import (
    build_generate_user_task_environment_models_payload,
)


def test_registry_contains_expected_evaluation_goals():
    goals = get_evaluation_goals()

    assert {goal.goal_id for goal in goals} == {
        "efficiency",
        "effectiveness_and_error_safety",
        "cognitive_demand",
        "profile_accessibility",
    }


def test_each_goal_references_known_dimensions():
    dimensions = {
        dimension.dimension_id
        for dimension in get_evaluation_dimensions()
    }

    for goal in get_evaluation_goals():
        assert set(goal.dimension_ids) <= dimensions


def test_each_dimension_references_known_metrics():
    for dimension in get_evaluation_dimensions():
        for metric_id in dimension.metric_ids:
            assert get_metric_by_id(metric_id) is not None


def test_predefined_metrics_provide_frontend_explanatory_content():
    for metric in get_predefined_evaluation_metrics():
        assert metric.name
        assert metric.description
        assert metric.analysis_question
        assert metric.data_basis
        assert metric.limitation


def test_frontend_metric_cards_use_plain_language_and_examples():
    cognitive_load = get_metric_by_id("cognitive_load")
    error_risk = get_metric_by_id("error_risk")

    cognitive_content = _metric_display_content(cognitive_load)
    error_content = _metric_display_content(error_risk)

    assert "mental" not in cognitive_content["description"].lower()
    assert "welche aussage" not in cognitive_content["description"].lower()
    assert "Konzentration" in cognitive_content["description"]
    assert "Gemessen wird" in cognitive_content["example"]
    assert "Pflichtfelder" in error_content["example"]
    assert "event" not in cognitive_content
    assert "limitation" not in error_content


def test_efficiency_resolves_to_expected_metrics():
    resolved = resolve_evaluation_goal_selection(
        EvaluationGoalSelection(selected_goal_ids=["efficiency"])
    )

    assert [
        metric.metric_id
        for metric in resolved.selected_metrics.selected_metrics
    ] == [
        "completion_time",
        "completion_efficiency",
        "time_limit_risk",
    ]


def test_multiple_goals_deduplicate_shared_metrics():
    resolved = resolve_evaluation_goal_selection(
        EvaluationGoalSelection(
            selected_goal_ids=[
                "cognitive_demand",
                "effectiveness_and_error_safety",
            ]
        )
    )

    metric_ids = [
        metric.metric_id
        for metric in resolved.selected_metrics.selected_metrics
    ]
    assert metric_ids.count("error_risk") == 1
    assert metric_ids == [
        "cognitive_load",
        "error_risk",
        "task_success_score",
    ]


def test_unknown_goal_id_is_rejected_clearly():
    with pytest.raises(ValueError, match="unknown_goal"):
        resolve_evaluation_goal_selection(
            EvaluationGoalSelection(selected_goal_ids=["unknown_goal"])
        )


def test_custom_metric_requests_are_preserved():
    resolved = resolve_evaluation_goal_selection(
        EvaluationGoalSelection(
            selected_goal_ids=["efficiency"],
            custom_metric_requests=["Wo entstehen Verzögerungen?"],
        )
    )

    assert resolved.custom_metric_requests == [
        "Wo entstehen Verzögerungen?"
    ]
    assert resolved.selected_metrics.custom_metric_requests == [
        "Wo entstehen Verzögerungen?"
    ]


def test_simulation_plan_contains_metrics_derived_from_goals():
    plan = prepare_simulation_plan_from_state(
        {
            "scenario_context": {"user_profiles": ["Generisch"]},
            "evaluation_goal_selection": {
                "selected_goal_ids": ["efficiency"],
                "custom_metric_requests": [],
            },
        }
    )

    assert plan is not None
    assert [metric.metric_id for metric in plan.evaluation_metrics] == [
        "completion_time",
        "completion_efficiency",
        "time_limit_risk",
    ]
    assert [goal.goal_id for goal in plan.evaluation_goals] == ["efficiency"]
    assert [
        dimension.dimension_id
        for dimension in plan.evaluation_dimensions
    ] == [
        "processing_time",
        "completion_efficiency",
        "time_limit_exceedance",
    ]


def test_profile_accessibility_uses_general_comparable_metrics():
    resolved = resolve_evaluation_goal_selection(
        EvaluationGoalSelection(selected_goal_ids=["profile_accessibility"])
    )

    metric_ids = [
        metric.metric_id
        for metric in resolved.selected_metrics.selected_metrics
    ]

    assert metric_ids == [
        "completion_time",
        "completion_efficiency",
        "task_success_score",
        "cognitive_load",
        "error_risk",
    ]


def test_existing_direct_metric_path_still_works():
    plan = prepare_simulation_plan_from_state(
        {
            "evaluation_metrics": {
                "selected_metrics": [
                    get_metric_by_id("cognitive_load").model_dump()
                ]
            }
        }
    )

    assert plan is not None
    assert [metric.metric_id for metric in plan.evaluation_metrics] == [
        "cognitive_load"
    ]
    assert plan.evaluation_goals == []
    assert plan.evaluation_dimensions == []


def test_frontend_goal_selection_builder_serializes_goal_ids():
    selection = build_evaluation_goal_selection(["efficiency"])

    assert selection == {
        "selected_goal_ids": ["efficiency"],
        "custom_metric_requests": [],
    }


def test_frontend_selection_bundle_contains_resolved_metrics():
    bundle = build_evaluation_selection_bundle(["efficiency"])

    assert bundle["evaluation_goal_selection"]["selected_goal_ids"] == [
        "efficiency"
    ]
    assert [
        metric["metric_id"]
        for metric in bundle["evaluation_metrics"]["selected_metrics"]
    ] == [
        "completion_time",
        "completion_efficiency",
        "time_limit_risk",
    ]


def test_frontend_metric_selection_bundle_contains_direct_metrics():
    bundle = build_metric_selection_bundle(
        ["cognitive_load", "completion_time"]
    )

    assert bundle["evaluation_goal_selection"] is None
    assert bundle["resolved_evaluation_selection"] is None
    assert [
        metric["metric_id"]
        for metric in bundle["evaluation_metrics"]["selected_metrics"]
    ] == [
        "cognitive_load",
        "completion_time",
    ]


def test_frontend_metric_selection_bundle_keeps_empty_selection_empty():
    bundle = build_metric_selection_bundle([])

    assert bundle["evaluation_goal_selection"] is None
    assert bundle["evaluation_metrics"] is None
    assert bundle["resolved_evaluation_selection"] is None


def test_frontend_payload_transfers_goal_selection():
    payload = build_generate_user_task_environment_models_payload(
        description="Test scenario",
        scenario_context={"user_profiles": ["Generisch"]},
        dimensions={},
        evaluation_goal_selection={"selected_goal_ids": ["efficiency"]},
    )

    assert payload["evaluation_goal_selection"] == {
        "selected_goal_ids": ["efficiency"]
    }
