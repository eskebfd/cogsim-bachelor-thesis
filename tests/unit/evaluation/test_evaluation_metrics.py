import pytest
from pydantic import ValidationError

from backend.domains.evaluation.schemas.evaluation_metrics import (
    EvaluationMetricDefinition,
    EvaluationMetricsSelection,
)
from backend.domains.evaluation.registries.metrics import (
    build_default_evaluation_metrics_selection,
    get_metric_by_id,
    get_predefined_evaluation_metrics,
)


def metric_payload() -> dict:
    return {
        "metric_id": "attention_drop_events",
        "name": "Attention Drop Events",
        "description": "Zählt deutliche Aufmerksamkeitsabfälle.",
        "metric_type": "event",
        "source": "suggested",
        "expected_output_range": [0, 20],
    }


def test_evaluation_metric_definition_validates():
    metric = EvaluationMetricDefinition.model_validate(metric_payload())

    assert metric.metric_type == "event"
    assert metric.expected_output_range == (0, 20)
    assert metric.requires_simulation is True


def test_selection_requires_at_least_one_metric():
    with pytest.raises(ValidationError):
        EvaluationMetricsSelection(selected_metrics=[])


def test_custom_metric_with_analysis_question_is_supported():
    payload = metric_payload()
    payload.update(
        {
            "metric_id": "custom_reorientation_delay",
            "name": "Reorientation Delay",
            "source": "custom",
            "metric_type": "time",
            "analysis_question": "Wie lange dauert die Neuorientierung?",
        }
    )

    metric = EvaluationMetricDefinition.model_validate(payload)

    assert metric.source == "custom"
    assert metric.analysis_question == "Wie lange dauert die Neuorientierung?"


def test_expected_output_range_rejects_reversed_bounds():
    payload = metric_payload()
    payload["expected_output_range"] = [100, 0]

    with pytest.raises(ValidationError):
        EvaluationMetricDefinition.model_validate(payload)


def test_registry_contains_all_predefined_metrics():
    metrics = get_predefined_evaluation_metrics()

    assert {metric.metric_id for metric in metrics} == {
        "cognitive_load",
        "error_risk",
        "completion_efficiency",
        "task_success_score",
        "completion_time",
        "time_limit_risk",
    }


def test_profile_load_factors_are_not_selectable_evaluation_metrics():
    metric_ids = {
        metric.metric_id for metric in get_predefined_evaluation_metrics()
    }

    assert "dyslexia_reading_load" not in metric_ids
    assert "adhd_interaction_load" not in metric_ids


def test_get_metric_by_id_returns_copy_or_none():
    metric = get_metric_by_id("error_risk")

    assert metric is not None
    assert metric.metric_id == "error_risk"
    assert metric.name == "Fehlerrisiko"
    assert metric.metric_type == "score"
    assert "nicht empirisch kalibriert" in metric.description
    assert get_metric_by_id("unknown_metric") is None


def test_task_success_metric_is_displayed_as_score():
    metric = get_metric_by_id("task_success_score")

    assert metric is not None
    assert metric.metric_id == "task_success_score"
    assert metric.name == "Aufgabenerfolgswert"
    assert metric.metric_type == "score"
    assert "keine statistisch kalibrierte" in metric.description


def test_legacy_task_success_probability_metric_id_resolves_to_score():
    metric = get_metric_by_id("task_success_probability")
    selection = build_default_evaluation_metrics_selection(
        ["task_success_probability", "task_success_score"]
    )

    assert metric is not None
    assert metric.metric_id == "task_success_score"
    assert [item.metric_id for item in selection.selected_metrics] == [
        "task_success_score"
    ]


def test_time_limit_risk_metric_is_displayed_as_score():
    metric = get_metric_by_id("time_limit_risk")

    assert metric is not None
    assert metric.metric_type == "score"
    assert "keine empirisch kalibrierte Wahrscheinlichkeit" in metric.description


def test_build_default_evaluation_metrics_selection():
    default_selection = build_default_evaluation_metrics_selection()
    selection = build_default_evaluation_metrics_selection(
        ["cognitive_load", "completion_time"]
    )

    assert len(default_selection.selected_metrics) == 6
    assert [metric.metric_id for metric in selection.selected_metrics] == [
        "cognitive_load",
        "completion_time",
    ]
    assert selection.custom_metric_requests == []
