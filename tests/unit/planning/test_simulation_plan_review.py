from types import SimpleNamespace

import frontend.features.computed_parameters.simulation_plan_review as plan_review
from backend.workflow.nodes import review_nodes


def minimal_plan() -> dict:
    return {
        "selected_user_profiles": [
            {
                "profile_id": "generic",
                "label": "Generic",
                "is_baseline": True,
            }
        ],
        "evaluation_metrics": [
            {
                "metric_id": "cognitive_load",
                "name": "Cognitive Load",
                "metric_type": "score",
            }
        ],
        "required_models": [
            {
                "model_type": "task",
                "instance_scope": "shared",
                "required": True,
            }
        ],
    }


def test_simulation_plan_review_data_contains_core_sections():
    review_data = plan_review.build_simulation_plan_review_data(minimal_plan())

    assert review_data["selected_user_profiles"][0]["Profile ID"] == "generic"
    assert review_data["evaluation_metrics"][0]["Metric ID"] == (
        "cognitive_load"
    )
    assert review_data["required_models"][0]["Model"] == "task"


def test_simulation_plan_review_can_render_minimal_plan(monkeypatch):
    rendered_markup = []
    rendered_tables = []
    fake_streamlit = SimpleNamespace(
        markdown=lambda body, *args, **kwargs: rendered_markup.append(body),
        dataframe=lambda rows, *args, **kwargs: rendered_tables.append((rows, kwargs)),
        warning=lambda *args, **kwargs: None,
        caption=lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(plan_review, "st", fake_streamlit)

    review_data = plan_review.render_simulation_plan_review(minimal_plan())

    markup = "".join(rendered_markup)
    assert "Nutzerprofile" in markup
    assert "Ausgewählte Auswertungswerte" in markup
    assert "Verwendete Grundlagen" in markup
    assert len(rendered_tables) == 3
    assert rendered_tables[0][0][0]["Profile ID"] == "generic"
    assert rendered_tables[0][1]["use_container_width"] is True
    assert review_data["selected_user_profiles"]


def test_backend_review_node_preserves_simulation_plan(monkeypatch):
    monkeypatch.setattr(
        review_nodes,
        "generate_revision_instruction",
        lambda **kwargs: SimpleNamespace(
            model_dump=lambda: {"revision_instruction": "Überarbeiten"}
        ),
    )
    state = {
        "scenario_description": "Test scenario",
        "current_stage": "review_base_task",
        "feedback_target": "task_model",
        "feedback": {"note": "Test"},
        "simulation_plan": minimal_plan(),
    }

    result = review_nodes.prepare_revision_instruction_node(state)

    assert result["simulation_plan"] == minimal_plan()
    assert result["revision_instruction"] == "Überarbeiten"
