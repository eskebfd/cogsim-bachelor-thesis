from frontend.features.dimensions.section import (
    SIGNAL_GROUPS,
    build_detected_scenario_context,
    definition_for_signal,
    selected_label_for_value,
)
from frontend.features.user_profiles.section import (
    PROFILE_CARD_CONTENT,
    normalize_user_profiles,
    toggle_user_profile,
)
from frontend.features.evaluation_goals.section import (
    build_metrics_selection,
)
from frontend.features.models.user_profile_summary import USER_MODEL_READONLY_NOTICE


def test_normalize_user_profiles_defaults_to_generic():
    assert normalize_user_profiles([]) == ["Generisch"]


def test_normalize_user_profiles_adds_generic_baseline_for_specific_profiles():
    assert normalize_user_profiles(["ADHS"]) == [
        "Generisch",
        "ADHS",
    ]


def test_normalize_user_profiles_preserves_adhd_and_dyslexia():
    assert normalize_user_profiles(
        ["ADHS", "Dyslexie"]
    ) == [
        "Generisch",
        "ADHS",
        "Dyslexie",
    ]


def test_toggle_user_profile_preserves_multiple_specific_profiles():
    profiles = toggle_user_profile(["Generisch"], "ADHS")
    profiles = toggle_user_profile(profiles, "Dyslexie")

    assert profiles == [
        "Generisch",
        "ADHS",
        "Dyslexie",
    ]


def test_toggle_user_profile_keeps_generic_baseline_active():
    assert toggle_user_profile(["Generisch", "ADHS"], "Generisch") == [
        "Generisch",
        "ADHS",
    ]


def test_profile_cards_define_professional_metadata_for_each_profile():
    assert set(PROFILE_CARD_CONTENT) == {
        "Generisch",
        "ADHS",
        "Dyslexie",
    }
    assert PROFILE_CARD_CONTENT["Generisch"]["footer_label"] == "Baseline"
    assert PROFILE_CARD_CONTENT["ADHS"]["footer_label"] == "ADHS auswählen"
    assert (
        PROFILE_CARD_CONTENT["Dyslexie"]["footer_label"]
        == "Dyslexie auswählen"
    )
    assert all("title" in content for content in PROFILE_CARD_CONTENT.values())
    assert all("description" in content for content in PROFILE_CARD_CONTENT.values())
    assert all("icon" in content for content in PROFILE_CARD_CONTENT.values())


def test_selected_label_for_numeric_dimension_value():
    assert selected_label_for_value(0) == "Sehr niedrig"
    assert selected_label_for_value(49) == "Niedrig bis moderat"
    assert selected_label_for_value(50) == "Deutlich vorhanden"
    assert selected_label_for_value(100) == "Stark ausgeprägt"


def test_dimension_definition_uses_signal_description_or_fallback():
    assert (
        definition_for_signal(
            {"description": "Technischer Beschreibungstext"},
            "reading_demand",
        )
        == "Wie viel gelesen und verstanden werden muss."
    )
    assert definition_for_signal({"description": "Erklärung"}) == "Erklärung"
    assert "Skala von 0 bis 100" in definition_for_signal({})


def test_dimension_tabs_contain_no_user_dimensions():
    assert SIGNAL_GROUPS == [
        ("task_signals", "Aufgabe"),
        ("interface_signals", "Interface"),
        ("environment_signals", "Umgebung"),
    ]


def test_metrics_selection_contains_only_predefined_metrics():
    selection = build_metrics_selection(["cognitive_load", "error_risk"])

    assert [
        metric["metric_id"] for metric in selection["selected_metrics"]
    ] == ["cognitive_load", "error_risk"]
    assert selection["custom_metric_requests"] == []


def test_metrics_selection_can_be_empty_without_default_fallback():
    selection = build_metrics_selection([])

    assert selection == {
        "selected_metrics": [],
        "custom_metric_requests": [],
    }


def test_detected_context_uses_task_device_and_environment_only():
    context = build_detected_scenario_context(
        {
            "detected_device": "Laptop",
            "primary_task": {"label": "Anmelden", "description": "Kurs wählen"},
            "environment_options": [
                {"label": "Arbeitsplatz", "description": "Benachrichtigungen"}
            ],
        }
    )

    assert context == {
        "device": "Laptop",
        "task": {"label": "Anmelden", "description": "Kurs wählen"},
        "environment": "Arbeitsplatz: Benachrichtigungen",
    }


def test_user_model_readonly_notice_explains_locked_profile_values():
    assert "Referenzannahmen" in USER_MODEL_READONLY_NOTICE
    assert "nicht verändert" in USER_MODEL_READONLY_NOTICE
