from frontend.features.models import actions as model_actions
import frontend.state as state_module


class FakeSessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc

    def __setattr__(self, key, value):
        self[key] = value


def attribute(value: int) -> dict:
    return {
        "value": value,
        "scale_min_description": "niedrig",
        "scale_max_description": "hoch",
        "explanation": "Metadaten bleiben erhalten",
        "confidence": "high",
    }


def test_prepare_simulation_ignores_stale_model_draft_values(monkeypatch):
    captured = {}
    session_state = FakeSessionState(
        {
            "session_id": "session-1",
            "scenario_input": "Test scenario",
            "base_model_preview": {
                "user_model": {"name": "User"},
                "user_models": {},
                "task_model": {"task_complexity": attribute(30)},
                "interface_model": {"visual_clutter": attribute(20)},
                "environment_model": {"noise_level": attribute(20)},
            },
            "backend_state": {
                "simulation_plan": {"evaluation_metrics": []},
                "evaluation_goal_selection": None,
                "evaluation_metrics": {"selected_metrics": []},
            },
            "model_draft_updates": {
                "task": {"task_complexity": 68},
                "interface": {"visual_clutter": 55},
                "environment": {"noise_level": 70},
            },
        }
    )

    monkeypatch.setattr(model_actions.st, "session_state", session_state)
    monkeypatch.setattr(state_module.st, "session_state", session_state)
    monkeypatch.setattr(model_actions.st, "error", lambda *args, **kwargs: None)
    monkeypatch.setattr(model_actions.st, "rerun", lambda: None)

    def fake_prepare_simulation_workflow(**kwargs):
        captured.update(kwargs)
        return {
            "current_stage": "computed_parameters",
            "computed_parameters": {},
        }

    monkeypatch.setattr(
        model_actions,
        "prepare_simulation_workflow",
        fake_prepare_simulation_workflow,
    )

    model_actions.prepare_simulation()

    assert captured["task_model"]["task_complexity"]["value"] == 30
    assert captured["interface_model"]["visual_clutter"]["value"] == 20
    assert captured["environment_model"]["noise_level"]["value"] == 20
    assert (
        captured["environment_model"]["noise_level"]["explanation"]
        == "Metadaten bleiben erhalten"
    )
