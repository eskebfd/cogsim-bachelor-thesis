from frontend.features.simulation.results import (
    build_additional_timeline_rows,
    build_available_timeline_metric_options,
    build_compact_timeline_rows,
    build_display_profile_views,
    build_metric_chart_rows,
    build_overview_event_legend_rows,
    build_overview_duration_chart_rows,
    build_overview_metric_chart_rows,
    build_overview_metric_timeline_rows,
    build_profile_comparison_rows,
    build_profile_metric_timeline_rows,
    build_result_tab_labels,
    build_selected_timeline_metric_options,
    build_timeline_chart_rows,
    build_timeline_event_flag_rows,
)
from frontend.features.simulation.components.insights import (
    build_profile_recommendation_cards,
)
from frontend.features.simulation.components import data as data_component
from frontend.features.simulation.components import summary as summary_component


class FakeStreamlit:
    def __init__(self):
        self.markdown_calls = []

    def markdown(self, body, **kwargs):
        self.markdown_calls.append((body, kwargs))


def profile_result(
    profile_id: str,
    label: str,
    attention: float,
    recommendation: str,
) -> dict:
    timeline = [
        {
            "timestamp": "00:01",
            "current_task_step": {
                "step_id": "step_1",
                "name": "Lesen",
                "description": "Erste Seite lesen",
                "step_index": 0,
            },
            "reading_speed": 60,
            "attention": attention,
            "fatigue": 30,
            "cognitive_load": 55,
            "error_risk": 40,
            "task_success_score": 70,
            "completion_efficiency": 65,
            "events": [{"event_type": "very_low_attention"}],
        }
    ]
    return {
        "profile_id": profile_id,
        "profile_label": label,
        "initial_user_state": {"attention": attention + 10, "fatigue": 10},
        "final_state": {
            "attention": attention,
            "fatigue": 30,
            "reading_speed": 60,
        },
        "metrics": {
            "cognitive_load": 55,
            "error_risk": 40,
            "task_success_score": 70,
            "completion_efficiency": 65,
        },
        "events": [
            {
                "event_type": "very_low_attention",
                "step_id": "step_1",
            }
        ],
        "timeline": timeline,
        "problems": [f"Problem {label}"],
        "recommendations": [recommendation],
        "recommendation_cards": [
            {
                "title": "Orientierung und nächste Aktion deutlicher machen",
                "priority": "mittel",
                "finding": f"{label} zeigt eine Auffälligkeit.",
                "affected_step": "Step 1 – Erste Seite lesen",
                "reasoning": (
                    "Die Empfehlung wurde vom Backend aus Timeline, Events "
                    "und Schrittzeiten abgeleitet."
                ),
                "suggested_actions": [
                    "primäre nächste Aktion visuell hervorheben",
                ],
                "evidence": ["niedrigste Aufmerksamkeit 40 von 100"],
                "confidence": "mittel",
                "source_rule_ids": ["attention_drop"],
            }
        ],
        "positive_findings": [],
        "completion_time_seconds": 1,
        "actual_processing_duration_seconds": 1,
    }


def multi_profile_payload() -> dict:
    generic = profile_result("generic", "Generic", 70, "Texte kürzen")
    adhd = profile_result(
        "adhd",
        "ADHS",
        40,
        "Visuelle Ablenkungen reduzieren",
    )
    dyslexie = profile_result("dyslexie", "Dyslexie", 60, "Texte kürzen")
    return {
        "simulation_results": {
            "baseline_profile_id": "generic",
            "results_by_profile": {
                "generic": generic,
                "adhd": adhd,
                "dyslexie": dyslexie,
            },
        }
    }


def test_result_tabs_include_only_simulated_profiles_without_comparison_tab():
    profiles = build_display_profile_views(multi_profile_payload())

    assert build_result_tab_labels(profiles) == [
        "Überblick",
        "Generic",
        "ADHS",
        "Dyslexie",
    ]


def test_profile_comparison_contains_all_final_values():
    profiles = build_display_profile_views(multi_profile_payload())
    rows = build_profile_comparison_rows(profiles)

    assert [row["Profil"] for row in rows] == ["Generic", "ADHS", "Dyslexie"]
    assert rows[1]["Final Attention"] == 40
    assert rows[1]["Anzahl Events"] == 1
    assert "Task Success Score" in rows[1]
    assert rows[1]["Completion Time (s)"] == 1


def test_profile_views_use_final_metrics_when_metrics_key_is_missing():
    payload = multi_profile_payload()
    generic = payload["simulation_results"]["results_by_profile"]["generic"]
    generic["final_metrics"] = {
        **generic.pop("metrics"),
    }

    profiles = build_display_profile_views(payload)
    rows = build_profile_comparison_rows(profiles)

    assert rows[0]["Profil"] == "Generic"
    assert "Dyslexia Reading Load" not in rows[0]
    assert "ADHS Interaction Load" not in rows[0]


def test_result_chart_rows_use_existing_profile_values():
    profiles = build_display_profile_views(multi_profile_payload())

    metric_rows = build_overview_metric_chart_rows(profiles)
    duration_rows = build_overview_duration_chart_rows(profiles)

    assert metric_rows[0]["Profil"] == "Generic"
    assert metric_rows[0]["Cognitive Load"] == 55
    assert metric_rows[0]["Task Success Score"] == 70
    assert duration_rows[1]["Profil"] == "ADHS"
    assert duration_rows[1]["Completion Time (s)"] == 1
    assert duration_rows[1]["Events"] == 1


def test_profile_chart_rows_use_metrics_and_timeline_values():
    profile = build_display_profile_views(multi_profile_payload())[0]

    metric_rows = build_metric_chart_rows(profile["metrics"])
    timeline_rows = build_timeline_chart_rows(profile["timeline"])

    assert {"Metrik": "Kognitive Belastung", "Wert": 55} in metric_rows
    assert timeline_rows[0]["Attention"] == 70
    assert timeline_rows[0]["Reading Speed"] == 60


def test_metric_timeline_rows_use_steps_on_x_axis_and_bounded_metric_values():
    profile = profile_result("generic", "Generic", 70, "Texte kürzen")
    profile["timeline"] = [
        {
            "timestamp": "00:02",
            "current_task_step": {
                "step_id": "step_1",
                "name": "Lesen",
                "description": "Erste Seite lesen",
                "step_index": 0,
            },
            "attention": 95,
            "error_risk": 20,
            "events": [],
        },
        {
            "timestamp": "00:05",
            "current_task_step": {
                "step_id": "step_2",
                "name": "Formular",
                "description": "Pflichtfelder ausfüllen",
                "step_index": 1,
            },
            "attention": 120,
            "error_risk": 55,
            "events": [{"event_type": "high_error_risk"}],
        },
    ]

    rows = build_profile_metric_timeline_rows(profile, ["attention", "error_risk"])
    event_rows = build_timeline_event_flag_rows([profile])

    assert rows == [
        {
            "Profil": "Generic",
            "Metrik": "Aufmerksamkeit",
            "Metric ID": "attention",
            "Step": "Step 1",
            "Step Detail": "Step 1 – Erste Seite lesen",
            "Step Order": 1,
            "Wert": 95.0,
        },
        {
            "Profil": "Generic",
            "Metrik": "Fehlerrisiko",
            "Metric ID": "error_risk",
            "Step": "Step 1",
            "Step Detail": "Step 1 – Erste Seite lesen",
            "Step Order": 1,
            "Wert": 20.0,
        },
        {
            "Profil": "Generic",
            "Metrik": "Aufmerksamkeit",
            "Metric ID": "attention",
            "Step": "Step 2",
            "Step Detail": "Step 2 – Pflichtfelder ausfüllen",
            "Step Order": 2,
            "Wert": 100,
        },
        {
            "Profil": "Generic",
            "Metrik": "Fehlerrisiko",
            "Metric ID": "error_risk",
            "Step": "Step 2",
            "Step Detail": "Step 2 – Pflichtfelder ausfüllen",
            "Step Order": 2,
            "Wert": 55.0,
        },
    ]
    assert event_rows == [
        {
            "Profil": "Generic",
            "Step": "Step 2",
            "Step Detail": "Step 2 – Pflichtfelder ausfüllen",
            "Step Order": 2,
            "Event": "Erhöhter Fehlerrisiko-Score",
            "Event Details": "Generic: Erhöhter Fehlerrisiko-Score",
            "Event Erklärung": "Dieses Event markiert eine auffällige Situation im Aufgabenverlauf.",
            "Event Kurzinfo": "2. Erhöhter Fehlerrisiko-Score",
            "Event Tooltip": "1 Event: 2. Erhöhter Fehlerrisiko-Score",
            "Event Symbols": "②",
            "Event Types": "high_error_risk",
            "Event Icon Items": [
                {
                    "symbol": "②",
                    "label": "Erhöhter Fehlerrisiko-Score",
                    "description": "Dieses Event markiert eine auffällige Situation im Aufgabenverlauf.",
                }
            ],
            "Event Count": 1,
            "Wert": 96,
            "Event Y": 104,
        }
    ]


def test_profile_event_rows_format_values_and_thresholds_for_german_ui():
    profile = profile_result("generic", "Generic", 70, "Texte kürzen")
    profile["timeline"][0]["events"] = [
        {
            "event_type": "high_error_risk",
            "value": 63.9,
            "threshold": 60.0,
        }
    ]

    rows = build_overview_event_legend_rows([profile])

    assert rows[0]["value"] == "63,9 von 100"
    assert rows[0]["threshold"] == "Fehlerrisiko: mindestens 60 von 100"
    assert rows[0]["trigger"] == "Fehlerrisiko: mindestens 60 von 100"


def test_overview_metric_timeline_groups_profiles_by_selected_metric():
    profiles = build_display_profile_views(multi_profile_payload())
    rows = build_overview_metric_timeline_rows(profiles, "error_risk")

    assert [row["Profil"] for row in rows] == ["Generic", "ADHS", "Dyslexie"]
    assert {row["Metrik"] for row in rows} == {"Fehlerrisiko"}
    assert {row["Step"] for row in rows} == {"Step 1"}


def test_available_timeline_metrics_only_include_present_numeric_metrics():
    profiles = build_display_profile_views(multi_profile_payload())
    options = build_available_timeline_metric_options(profiles)

    assert {"id": "error_risk", "label": "Fehlerrisiko"} in options
    assert {"id": "cognitive_load", "label": "Kognitive Belastung"} in options


def test_selected_timeline_metrics_respect_explicit_metric_selection():
    profiles = build_display_profile_views(multi_profile_payload())

    selected_options = build_selected_timeline_metric_options(
        profiles,
        {"error_risk"},
    )
    no_timeline_options = build_selected_timeline_metric_options(
        profiles,
        {"completion_time"},
    )
    legacy_options = build_selected_timeline_metric_options(profiles, None)

    assert selected_options == [{"id": "error_risk", "label": "Fehlerrisiko"}]
    assert no_timeline_options == []
    assert {"id": "cognitive_load", "label": "Kognitive Belastung"} in legacy_options


def test_selected_metric_ids_prefer_explicit_selection_over_plan_fallback(
    monkeypatch,
):
    class SessionState(dict):
        pass

    fake_streamlit = type(
        "FakeStreamlit",
        (),
        {
            "session_state": SessionState(
                {
                    "evaluation_metrics": {
                        "selected_metrics": [
                            {"metric_id": "cognitive_load"},
                            {"metric_id": "completion_efficiency"},
                        ]
                    },
                    "backend_state": {
                        "simulation_plan": {
                            "evaluation_metrics": [
                                {"metric_id": "cognitive_load"},
                                {"metric_id": "error_risk"},
                                {"metric_id": "completion_efficiency"},
                                {"metric_id": "task_success_score"},
                            ]
                        }
                    },
                }
            )
        },
    )()
    monkeypatch.setattr(data_component, "st", fake_streamlit)

    assert data_component.selected_metric_ids_from_session() == {
        "cognitive_load",
        "completion_efficiency",
    }


def test_profile_metric_chart_rows_respect_selected_metrics():
    profile = build_display_profile_views(multi_profile_payload())[0]

    metric_rows = build_metric_chart_rows(
        profile["metrics"],
        {"error_risk"},
    )

    assert metric_rows == [{"Metrik": "Fehlerrisiko", "Wert": 40}]


def test_results_view_reads_legacy_task_success_probability_values():
    profile = profile_result("generic", "Generic", 70, "Texte kürzen")
    profile["metrics"].pop("task_success_score")
    profile["metrics"]["task_success_probability"] = 72
    profile["timeline"][0].pop("task_success_score")
    profile["timeline"][0]["task_success_probability"] = 72

    display_profile = build_display_profile_views(profile)[0]
    comparison = build_profile_comparison_rows([display_profile])
    additional_rows = build_additional_timeline_rows(display_profile["timeline"])

    assert comparison[0]["Task Success Score"] == 72
    assert additional_rows[0]["Task Success Score"] == 72


def test_profile_recommendation_cards_are_grouped_by_profile_data():
    profiles = build_display_profile_views(multi_profile_payload())
    recommendation_cards = {
        profile["profile_label"]: build_profile_recommendation_cards(profile)
        for profile in profiles
    }

    assert set(recommendation_cards) == {"Generic", "ADHS", "Dyslexie"}
    assert all(recommendation_cards.values())
    assert "Auffälligkeit" in recommendation_cards["ADHS"][0]["finding"]
    assert recommendation_cards["ADHS"][0]["reasoning"]
    assert recommendation_cards["ADHS"][0]["suggested_actions"]


def test_timeline_is_filtered_by_selected_profile_before_rendering():
    profiles = build_display_profile_views(multi_profile_payload())
    adhd = next(profile for profile in profiles if profile["profile_id"] == "adhd")
    rows = build_compact_timeline_rows(adhd["timeline"])

    assert len(rows) == 1
    assert rows[0]["Attention"] == 40
    assert list(rows[0]) == [
        "Time",
        "Profile",
        "Task Step",
        "Task Progress (%)",
        "Base Step Duration (s)",
        "Estimated Step Duration (s)",
        "Attention",
        "Fatigue",
        "Cognitive Load",
        "Error Risk Score",
        "Events",
    ]
    assert build_additional_timeline_rows(adhd["timeline"])[0]["Task Step"] == (
        "Step 1 – Erste Seite lesen"
    )


def test_single_profile_result_keeps_compact_profile_view():
    single = profile_result("generic", "Generic", 70, "Texte kürzen")
    profiles = build_display_profile_views(single)

    assert len(profiles) == 1
    assert profiles[0]["profile_id"] == "generic"
    assert build_result_tab_labels(profiles) == [
        "Überblick",
        "Generic",
    ]


def test_aborted_profile_status_is_available_to_results_view():
    aborted = profile_result("adhd", "ADHS", 20, "Ablenkungen reduzieren")
    aborted.update(
        {
            "completed": False,
            "abort_reason": "Maximum step duration exceeded",
            "aborted_step_id": "step_1",
            "aborted_step_name": "Hinweistext lesen",
            "allowed_step_duration": 60,
            "actual_step_duration": 60,
        }
    )

    profile = build_display_profile_views(aborted)[0]
    comparison = build_profile_comparison_rows([profile])[0]

    assert profile["completed"] is False
    assert profile["abort_reason"] == "Maximum step duration exceeded"
    assert profile["allowed_step_duration"] == 60
    assert profile["actual_step_duration"] == 60
    assert comparison["Status"] == "Abgebrochen"
    assert comparison["Abgebrochener Task Step"] == "Hinweistext lesen"


def test_overview_kpi_cards_render_with_missing_presentation_summary(monkeypatch):
    fake_streamlit = FakeStreamlit()
    monkeypatch.setattr(summary_component, "st", fake_streamlit)
    profiles = build_display_profile_views(multi_profile_payload())

    summary_component.render_overview_kpi_cards(
        profiles,
        presentation={"sections": {}},
    )

    rendered = fake_streamlit.markdown_calls[0][0]
    assert "Kurze Zusammenfassung" in rendered
    assert "Auffälligkeiten" in rendered
    assert "3 Nutzerprofile verglichen" in rendered


def test_overview_kpi_cards_hide_accidental_html_tag_text(monkeypatch):
    fake_streamlit = FakeStreamlit()
    monkeypatch.setattr(summary_component, "st", fake_streamlit)
    profiles = build_display_profile_views(multi_profile_payload())

    summary_component.render_overview_kpi_cards(
        profiles,
        presentation={
            "summary": {
                "status": {
                    "severity": "success",
                    "label": "Simulation abgeschlossen",
                    "explanation": "Alle Profile wurden berechnet.",
                    "details": "**</DIV>**",
                },
                "primary_completion_time": {
                    "label": "Simulierte Bearbeitungszeit",
                    "value_label": "99 Sek.",
                    "basis_label": "längste simulierte Bearbeitungszeit",
                    "goms_basis_label": "54 Sek.",
                    "deviation_label": "+45 Sek.",
                    "explanation": "Die Simulation berücksichtigt zusätzliche Belastungen.",
                },
                "secondary_items": [],
                "explanation": "Zusammenfassung",
            }
        },
    )

    rendered = fake_streamlit.markdown_calls[0][0]
    assert "Simulation abgeschlossen" in rendered
    assert "</DIV>" not in rendered
