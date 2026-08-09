from contextlib import nullcontext
from types import SimpleNamespace
import inspect

import frontend.features.models.simulation_foundations as simulation_foundations
import frontend.features.models.environment_summary as environment_summary
import frontend.features.models.interface_summary as interface_summary
import frontend.features.models.user_profile_summary as user_profile_summary
from frontend.features.models.environment_summary import (
    build_environment_attribute_rows,
)
from frontend.features.models.interface_summary import (
    build_interface_attribute_rows,
)
from frontend.features.models.task_flow_summary import build_task_step_rows


def attribute(value: int, explanation: str) -> dict:
    return {
        "value": value,
        "scale_min_description": "Minimum",
        "scale_max_description": "Maximum",
        "explanation": explanation,
        "confidence": "high",
    }


def user_model(label: str, offset: int) -> dict:
    return {
        "user_type": label,
        "reading_difficulty": attribute(10 + offset, "Lesen"),
        "attention_stability": attribute(80 - offset, "Aufmerksamkeit"),
        "working_memory_stability": attribute(75 - offset, "Arbeitsgedächtnis"),
        "distraction_sensitivity": attribute(20 + offset, "Ablenkung"),
        "task_switching_difficulty": attribute(25 + offset, "Wechsel"),
        "vigilance_stability": attribute(78 - offset, "Daueraufmerksamkeit"),
        "inhibitory_control": attribute(76 - offset, "Inhibition"),
        "attention_switching_stability": attribute(74 - offset, "Aufmerksamkeitswechsel"),
        "divided_attention_capacity": attribute(72 - offset, "Geteilte Aufmerksamkeit"),
        "omission_tendency": attribute(18 + offset, "Auslassungen"),
        "reaction_variability": attribute(20 + offset, "Reaktionsschwankung"),
        "assumptions": [f"Annahme für {label}"],
    }


def test_user_models_build_selected_profile_comparison_table():
    models = {
        "generic": user_model("Generic", 0),
        "adhd": user_model("ADHS", 30),
    }

    rows = user_profile_summary.build_user_model_comparison_rows({}, models)

    assert list(rows[0]) == [
        "Attribut-ID",
        "Attribut",
        "Beschreibung",
        "Generic",
        "ADHS",
    ]
    assert [row["Attribut"] for row in rows] == [
        "Leseschwierigkeit",
        "Dekodierstabilität",
        "Orthografische Verarbeitungsstabilität",
        "Parallele Buchstabenverarbeitung",
        "Aufmerksamkeitsstabilität",
        "Arbeitsgedächtnisstabilität",
        "Ablenkungsempfindlichkeit",
        "Schwierigkeit beim Aufgabenwechsel",
        "Daueraufmerksamkeitsstabilität",
        "Inhibitionskontrolle",
        "Aufmerksamkeitswechsel-Stabilität",
        "Kapazität geteilter Aufmerksamkeit",
        "Auslassungstendenz",
        "Reaktionsschwankung",
    ]
    assert "Dyslexie" not in rows[0]
    assert rows[0]["Generic"] == 10
    assert rows[0]["ADHS"] == 40


def test_user_model_review_renders_comparison_cards(monkeypatch):
    rendered_markup = []
    fake_streamlit = SimpleNamespace(
        markdown=lambda body, *args, **kwargs: rendered_markup.append(body),
        caption=lambda *args, **kwargs: None,
        warning=lambda *args, **kwargs: None,
        write=lambda *args, **kwargs: None,
        expander=lambda *args, **kwargs: nullcontext(),
        container=lambda *args, **kwargs: nullcontext(),
        divider=lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(user_profile_summary, "st", fake_streamlit)

    user_profile_summary.render_user_model_review(
        {},
        {
            "generic": user_model("Generic", 0),
            "dyslexie": user_model("Dyslexie", 50),
        },
    )

    markup = "".join(rendered_markup)
    assert "cogsim-user-comparison-grid" in markup
    assert "Leseschwierigkeit" in markup
    assert "Generic" in markup
    assert "Dyslexie" in markup
    assert "Annahmen der Nutzerprofile" not in markup
    assert "Annahme für Generic" not in markup
    assert "Annahme für Dyslexie" not in markup


def test_task_steps_are_prepared_as_hta_goms_table():
    rows = build_task_step_rows(
        {
            "steps": [
                {
                    "name": "Hinweise lesen",
                    "description": "Informationen erfassen",
                    "operation_time_estimates": [
                        {
                            "operation": "read",
                            "estimated_duration_seconds": 8,
                        },
                        {
                            "operation": "think",
                            "estimated_duration_seconds": 2,
                        },
                    ],
                    "estimated_duration_seconds": 10,
                    "cognitive_requirements": ["lesen", "verstehen"],
                }
            ]
        }
    )

    assert rows == [
        {
            "Schritt": 1,
            "HTA-Schritt": "Hinweise lesen",
            "Beschreibung": "Informationen erfassen",
            "GOMS-Operationen": "lesen (8 s), nachdenken (2 s)",
            "Dauer": "10 s",
            "Kognitive Anforderungen": "lesen, verstehen",
        }
    ]


def test_interface_and_environment_models_build_compact_tables():
    interface_rows = build_interface_attribute_rows(
        {
            "text_volume": attribute(70, "Viele sichtbare Texte"),
            "sentence_length": attribute(60, "Längere Sätze"),
        }
    )
    environment_rows = build_environment_attribute_rows(
        {
            "noise_level": attribute(80, "Laute Umgebung"),
            "distractions": attribute(75, "Viele Benachrichtigungen"),
        }
    )

    assert interface_rows[0] == {
        "Attribut": "Textmenge",
        "Aktueller Wert": 70,
    }
    assert len(interface_rows) == 2
    assert environment_rows[0] == {
        "Attribut": "Geräuschpegel",
        "Aktueller Wert": 80,
    }
    assert len(environment_rows) == 2


def test_interface_summary_uses_model_value_and_ignores_old_slider_state():
    model = {"text_volume": attribute(40, "Alte Erklärung für Wert 40")}

    rows = build_interface_attribute_rows(model)

    assert rows[0] == {
        "Attribut": "Textmenge",
        "Aktueller Wert": 40,
    }
    assert "Bedeutung" not in rows[0]


def test_environment_summary_uses_model_value_only():
    model = {"noise_level": attribute(30, "Laute Umgebung")}

    rows = build_environment_attribute_rows(model)

    assert rows[0]["Attribut"] == "Geräuschpegel"
    assert rows[0]["Aktueller Wert"] == 30


def test_interface_and_environment_reviews_do_not_render_feedback_elements():
    interface_source = inspect.getsource(interface_summary)
    environment_source = inspect.getsource(environment_summary)

    assert "Feedback zum Interface-Modell" not in interface_source
    assert "Feedback zum Umgebungsmodell" not in environment_source
    assert "render_feedback_area" not in interface_source
    assert "render_feedback_area" not in environment_source


def test_model_review_renders_no_separate_slider_save_buttons():
    source = inspect.getsource(simulation_foundations)

    assert "Änderungen am Aufgabenmodell übernehmen" not in source
    assert "Änderungen am Interface-Modell übernehmen" not in source
    assert "Änderungen am Umgebungsmodell übernehmen" not in source
    assert "_render_direct_update_action" not in source


def test_model_overview_excludes_simulation_plan_tab_and_keeps_task_attribute_edit_action():
    assert "Simulationsplan" not in simulation_foundations.MODEL_TABS
    assert "Aufgabenparameter" not in simulation_foundations.MODEL_TABS
    assert "Aufgabenwerte" in simulation_foundations.MODEL_TABS
    assert "Aufgabenablauf" not in simulation_foundations.MODEL_TABS
    source = inspect.getsource(simulation_foundations)
    assert 'area="task"' in source
    assert "edit_action=lambda" in source
