from backend.domains.simulation.config import DEFAULT_SIMULATION_CONFIG
from backend.domains.simulation.presentation import build_result_presentation_view
from backend.domains.simulation.results import build_simulation_results


def _profile(
    profile_id: str = "generic",
    *,
    label: str = "Generic",
    completed: bool = True,
    completion_time: float = 90,
    planned_time: float = 60,
    events: list[dict] | None = None,
    recommendations: list[dict] | None = None,
    time_limit_seconds: float | None = None,
) -> dict:
    result = {
        "profile_id": profile_id,
        "profile_label": label,
        "completed": completed,
        "completion_time_seconds": completion_time,
        "task_step_durations": [
            {"planned_duration_seconds": planned_time / 2},
            {"planned_duration_seconds": planned_time / 2},
        ],
        "metrics": {
            "cognitive_load": 40,
            "error_risk": 30,
            "task_success_score": 82,
            "completion_efficiency": 75,
        },
        "events": events or [],
        "timeline": [],
        "recommendation_cards": recommendations or [],
    }
    if time_limit_seconds is not None:
        result["time_limit_seconds"] = time_limit_seconds
    return result


def test_presentation_uses_understandable_status_instead_of_ok():
    view = build_result_presentation_view([_profile()])

    status = view["summary"]["status"]

    assert status["label"] == "Simulation erfolgreich abgeschlossen"
    assert status["label"] != "OK"
    assert status["status_id"] == "completed_clear"


def test_presentation_status_for_findings_and_aborted_runs():
    finding_view = build_result_presentation_view(
        [
            _profile(
                events=[
                    {
                        "event_type": "very_low_attention",
                        "threshold": 65,
                        "value": 60,
                    }
                ]
            )
        ]
    )
    aborted_view = build_result_presentation_view(
        [_profile(completed=False)]
    )

    assert finding_view["summary"]["status"]["status_id"] == (
        "completed_with_findings"
    )
    assert aborted_view["summary"]["status"]["status_id"] == "aborted"


def test_presentation_completion_time_explains_slowest_profile_and_basis_time():
    view = build_result_presentation_view(
        [
            _profile(label="Generic", completion_time=80, planned_time=60),
            _profile(label="ADHS", completion_time=148, planned_time=90),
        ]
    )

    completion = view["summary"]["primary_completion_time"]

    assert completion["label"] == "Simulierte Bearbeitungszeit"
    assert completion["value_seconds"] == 148
    assert "ADHS" in completion["basis_label"]
    assert completion["goms_basis_seconds"] == 90
    assert completion["deviation_seconds"] == 58
    assert "Basiszeit" in completion["explanation"]


def test_presentation_has_three_secondary_summary_items():
    view = build_result_presentation_view(
        [_profile(), _profile("adhd", label="ADHS")]
    )

    items = view["summary"]["secondary_items"]

    assert len(items) == 3
    assert [item["item_id"] for item in items] == [
        "profiles",
        "task_success",
        "events",
    ]
    assert items[0]["label"] == "2 Nutzerprofile verglichen"


def test_metric_legend_is_complete_and_excludes_retired_metrics():
    view = build_result_presentation_view([_profile()])
    metric_ids = {item["metric_id"] for item in view["metric_legend"]}

    assert {
        "cognitive_load",
        "error_risk",
        "completion_time",
        "completion_efficiency",
        "task_success_score",
        "time_limit_risk",
    }.issubset(metric_ids)
    assert "dyslexia_reading_load" not in metric_ids
    assert "adhd_interaction_load" not in metric_ids
    cognitive_load = next(
        item for item in view["metric_legend"] if item["metric_id"] == "cognitive_load"
    )
    assert cognitive_load["preferred_direction"] == "niedriger ist günstiger"
    assert "Sehr hohe kognitive Belastung" in cognitive_load["related_events"]


def test_event_legend_uses_backend_thresholds():
    view = build_result_presentation_view([_profile()])
    high_error_risk = next(
        item for item in view["event_legend"] if item["event_id"] == "high_error_risk"
    )

    assert high_error_risk["trigger_value"] == str(
        DEFAULT_SIMULATION_CONFIG.event_thresholds["high_error_risk"]
    )
    assert "Fehlerrisiko ≥" in high_error_risk["trigger_description"]
    assert "Fehlerrisiko" in high_error_risk["related_metrics"]


def test_time_pressure_event_only_appears_with_explicit_time_limit():
    without_limit = build_result_presentation_view([_profile()])
    with_limit = build_result_presentation_view(
        [_profile(time_limit_seconds=120)]
    )

    assert "time_pressure_warning" not in {
        item["event_id"] for item in without_limit["event_legend"]
    }
    assert "time_pressure_warning" in {
        item["event_id"] for item in with_limit["event_legend"]
    }


def test_presentation_filters_metrics_and_events_by_selected_metrics():
    view = build_result_presentation_view(
        [_profile(time_limit_seconds=120)],
        selected_metric_ids={"cognitive_load"},
    )

    assert {item["metric_id"] for item in view["metric_legend"]} == {
        "cognitive_load"
    }
    assert {item["event_id"] for item in view["event_legend"]} == {
        "very_high_cognitive_load",
        "high_inhibition_load",
        "task_switching_strain",
    }


def test_simulation_results_keep_raw_events_but_filter_display_events():
    profile = _profile(
        events=[
            {"event_type": "very_high_cognitive_load"},
            {"event_type": "very_low_attention"},
        ],
    )
    profile["timeline"] = [
        {
            "timestamp": 1,
            "timestamp_seconds": 1,
            "current_task_step": {
                "step_id": "step_1",
                "step_index": 0,
                "name": "Prüfen",
            },
            "events": [
                {"event_type": "very_high_cognitive_load"},
                {"event_type": "very_low_attention"},
            ],
        }
    ]

    result = build_simulation_results(
        [profile],
        selected_metric_ids={"cognitive_load"},
    )
    rendered_profile = result["results_by_profile"]["generic"]

    assert len(rendered_profile["events"]) == 2
    assert rendered_profile["display_events"] == [
        {"event_type": "very_high_cognitive_load"}
    ]
    assert rendered_profile["display_timeline"][0]["events"] == [
        {"event_type": "very_high_cognitive_load"}
    ]


def test_simulation_results_filter_recommendations_by_selected_metrics():
    profile = _profile(
        recommendations=[
            {
                "title": "Belastung reduzieren",
                "structured_recommendation": {
                    "triggering_metric_ids": ["cognitive_load"],
                },
            },
            {
                "title": "Fehler vermeiden",
                "structured_recommendation": {
                    "triggering_metric_ids": ["error_risk"],
                },
            },
        ],
    )

    result = build_simulation_results(
        [profile],
        selected_metric_ids={"cognitive_load"},
    )
    rendered_profile = result["results_by_profile"]["generic"]

    assert [card["title"] for card in rendered_profile["recommendation_cards"]] == [
        "Belastung reduzieren"
    ]
    assert len(rendered_profile["raw_recommendation_cards"]) == 2
