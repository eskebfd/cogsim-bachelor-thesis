import frontend.state as state_module

from frontend.state import DEFAULT_SCENARIO, create_empty_backend_state


class FakeSessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc

    def __setattr__(self, key, value):
        self[key] = value


def test_default_scenario_contains_target_profiles_and_ux_factors():
    assert "ADHS" not in DEFAULT_SCENARIO
    assert "Dyslexie" not in DEFAULT_SCENARIO
    assert "Person" in DEFAULT_SCENARIO
    assert "Laptop" in DEFAULT_SCENARIO
    assert "Hotelbuchungsseite" in DEFAULT_SCENARIO
    assert "Unterkunft" in DEFAULT_SCENARIO
    assert "Hoteldetails" in DEFAULT_SCENARIO
    assert "Benachrichtigungen" in DEFAULT_SCENARIO
    assert "Zeitdruck" in DEFAULT_SCENARIO


def test_create_empty_backend_state_contains_core_fields():
    state = create_empty_backend_state()

    assert state["current_stage"] == "dimensions"
    assert state["scenario_context"] == {}
    assert state["task_model"] == {}
    assert state["user_model"] == {}
    assert state["user_models"] == {}
    assert state["interface_model"] == {}
    assert state["environment_model"] == {}
    assert state["evaluation_metrics"] is None
    assert state["simulation_plan"] is None
    assert state["computed_parameters"] == {}
    assert state["simulation_model"] == {}
    assert state["simulation_results"] == {}
    assert state["dimensions"] == {}


def test_apply_workflow_state_accepts_optional_evaluation_metrics(monkeypatch):
    session_state = FakeSessionState({"backend_state": {}})
    monkeypatch.setattr(state_module.st, "session_state", session_state)
    selection = {
        "selected_metrics": [
            {
                "metric_id": "cognitive_load",
                "name": "Cognitive Load",
                "description": "Kognitive Belastung.",
                "metric_type": "score",
                "source": "predefined",
            }
        ]
    }

    state_module.apply_workflow_state({"evaluation_metrics": selection})

    assert session_state.backend_state["evaluation_metrics"] == selection


def test_apply_workflow_state_accepts_optional_simulation_plan(monkeypatch):
    session_state = FakeSessionState({"backend_state": {}})
    monkeypatch.setattr(state_module.st, "session_state", session_state)
    plan = {"selected_user_profiles": [{"profile_id": "generic"}]}

    state_module.apply_workflow_state({"simulation_plan": plan})

    assert session_state.backend_state["simulation_plan"] == plan


def test_metrics_update_invalidates_dependent_plan(monkeypatch):
    session_state = FakeSessionState(
        {
            "backend_state": {
                "simulation_plan": {"old": True},
                "computed_parameters": {"old": True},
            },
            "user_profiles": ["Generisch"],
        }
    )
    monkeypatch.setattr(state_module.st, "session_state", session_state)

    from frontend.workflow.actions import update_modeling_setup_state

    update_modeling_setup_state(
        "Szenario",
        {"task_signals": {}},
        evaluation_metrics={"selected_metrics": [{"metric_id": "error_risk"}]},
    )

    assert session_state.backend_state["simulation_plan"] is None
    assert session_state.backend_state["computed_parameters"] == {}


def test_scenario_reset_can_preserve_preselected_metrics(monkeypatch):
    session_state = FakeSessionState(
        {
            "backend_state": {},
            "user_profiles": ["Generisch"],
            "user_profile": "Generisch",
            "evaluation_metrics": {
                "selected_metrics": [{"metric_id": "task_success_score"}]
            },
            "evaluation_goal_selection": {"selected_goal_ids": []},
        }
    )
    monkeypatch.setattr(state_module.st, "session_state", session_state)

    state_module.reset_generated_data(
        preserve_profiles=True,
        preserve_evaluation=True,
    )

    assert session_state.evaluation_metrics == {
        "selected_metrics": [{"metric_id": "task_success_score"}]
    }
    assert session_state.evaluation_goal_selection == {"selected_goal_ids": []}
    assert session_state.backend_state["evaluation_metrics"] == {
        "selected_metrics": [{"metric_id": "task_success_score"}]
    }


def test_create_empty_backend_state_contains_review_fields():
    state = create_empty_backend_state()

    assert "feedback_target" in state
    assert "feedback" in state
    assert "revision_instruction" in state
    assert "last_feedback" in state


def test_apply_workflow_state_updates_model_previews(monkeypatch):
    session_state = FakeSessionState()
    monkeypatch.setattr(state_module.st, "session_state", session_state)

    state_module.apply_workflow_state(
        {
            "current_stage": "computed_parameters",
            "user_model": {"name": "User"},
            "task_model": {"name": "Task"},
            "interface_model": {"name": "Interface"},
            "environment_model": {"name": "Environment"},
            "computed_parameters": {"name": "Computed Task Parameters"},
        },
        target_step=7,
    )

    assert session_state.backend_state["current_stage"] == "computed_parameters"
    assert session_state.base_model_preview == {
        "user_model": {"name": "User"},
        "task_model": {"name": "Task"},
        "interface_model": {"name": "Interface"},
        "environment_model": {"name": "Environment"},
    }
    assert session_state.computed_parameters_preview == {
        "computed_parameters": {"name": "Computed Task Parameters"},
        "simulation_model": {},
    }
    assert session_state.simulation_step == 7


def test_apply_workflow_state_keeps_profiled_user_models(monkeypatch):
    session_state = FakeSessionState()
    monkeypatch.setattr(state_module.st, "session_state", session_state)
    user_models = {
        "generic": {"user_type": "Generic"},
        "adhd": {"user_type": "ADHD"},
    }

    state_module.apply_workflow_state(
        {
            "user_model": user_models["generic"],
            "user_models": user_models,
        }
    )

    assert session_state.base_model_preview["user_model"] == user_models[
        "generic"
    ]
    assert list(session_state.base_model_preview["user_models"]) == [
        "generic",
        "adhd",
    ]


def test_apply_workflow_state_invalidates_downstream_models(monkeypatch):
    session_state = FakeSessionState(
        {
            "computed_parameters_preview": {
                "computed_parameters": {"old": True}
            },
            "simulation_result": {"results": {"completed": True}},
        }
    )
    monkeypatch.setattr(state_module.st, "session_state", session_state)

    state_module.apply_workflow_state(
        {
            "user_model": {"name": "User"},
            "task_model": {"name": "Task"},
            "environment_model": {"name": "Environment"},
            "last_feedback": {"feedback_target": "user_model"},
        },
        feedback_scope="base",
        invalidate_downstream=True,
    )

    assert session_state.computed_parameters_preview is None
    assert session_state.simulation_result is None
    assert session_state.last_base_model_feedback == {
        "feedback_target": "user_model"
    }


def test_apply_workflow_state_syncs_revised_task_attributes_to_dimensions(monkeypatch):
    session_state = FakeSessionState(
        {
            "backend_state": {},
            "dimensions": {
                "task_signals": {
                    "task_complexity": {"value": 40},
                    "orthographic_irregularity": {"value": 10},
                }
            },
            "dimension_value_task_signals_task_complexity": 40,
            "dimension_value_task_signals_orthographic_irregularity": 10,
        }
    )
    monkeypatch.setattr(state_module.st, "session_state", session_state)

    state_module.apply_workflow_state(
        {
            "task_model": {
                "task_complexity": {"value": 58},
                "orthographic_irregularity": {"value": 14},
            }
        },
        feedback_scope="base",
        invalidate_downstream=True,
    )

    assert session_state.dimensions["task_signals"]["task_complexity"]["value"] == 58
    assert (
        session_state.dimensions["task_signals"]["orthographic_irregularity"]["value"]
        == 14
    )
    assert session_state.dimension_value_task_signals_task_complexity == 58
    assert session_state.dimension_value_task_signals_orthographic_irregularity == 14
    assert session_state.backend_state["dimensions"] == session_state.dimensions


def test_apply_dimension_values_to_model_previews_updates_existing_models(monkeypatch):
    session_state = FakeSessionState(
        {
            "dimensions": {
                "task_signals": {
                    "sustained_attention_demand": {"value": 91},
                },
                "interface_signals": {
                    "visual_clutter": {"value": 64},
                },
                "environment_signals": {
                    "time_pressure": {"value": 37},
                },
            },
            "base_model_preview": {
                "task_model": {
                    "steps": [{"name": "Erhaltener Schritt"}],
                    "sustained_attention_demand": {"value": 75},
                },
                "interface_model": {"visual_clutter": {"value": 30}},
                "environment_model": {"time_pressure": {"value": 20}},
            },
            "backend_state": {
                "task_model": {
                    "steps": [{"name": "Erhaltener Schritt"}],
                    "sustained_attention_demand": {"value": 75},
                },
                "interface_model": {"visual_clutter": {"value": 30}},
                "environment_model": {"time_pressure": {"value": 20}},
                "computed_parameters": {"old": True},
                "simulation_results": {"old": True},
            },
            "computed_parameters_preview": {"old": True},
            "simulation_result": {"old": True},
        }
    )
    monkeypatch.setattr(state_module.st, "session_state", session_state)

    state_module.apply_dimension_values_to_model_previews()

    assert (
        session_state.base_model_preview["task_model"][
            "sustained_attention_demand"
        ]["value"]
        == 91
    )
    assert session_state.backend_state["task_model"]["steps"] == [
        {"name": "Erhaltener Schritt"}
    ]
    assert (
        session_state.backend_state["task_model"][
            "sustained_attention_demand"
        ]["value"]
        == 91
    )
    assert session_state.base_model_preview["interface_model"]["visual_clutter"][
        "value"
    ] == 64
    assert session_state.base_model_preview["environment_model"]["time_pressure"][
        "value"
    ] == 37
    assert session_state.computed_parameters_preview is None
    assert session_state.simulation_result is None
    assert session_state.backend_state["computed_parameters"] == {}
    assert session_state.backend_state["simulation_results"] == {}


def test_build_scenario_context_contains_user_profile_comparison(monkeypatch):
    session_state = FakeSessionState(
        {
            "user_profile": "Generisch, ADHS",
            "user_profiles": ["Generisch", "ADHS"],
            "comparison_baseline": "Generisch",
            "device": "Laptop",
            "detected_task": {"label": "Formular ausfüllen"},
            "environment": "Online-Portal",
        }
    )
    monkeypatch.setattr(state_module.st, "session_state", session_state)

    context = state_module.build_scenario_context("Test scenario")

    assert context["user_profile"] == "Generisch, ADHS"
    assert context["user_profiles"] == ["Generisch", "ADHS"]
    assert context["comparison_baseline"] == "Generisch"
    assert "selected_metrics" not in context
    assert "task_parameters" not in context
