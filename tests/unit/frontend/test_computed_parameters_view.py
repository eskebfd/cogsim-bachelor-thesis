from contextlib import contextmanager
from types import SimpleNamespace

import frontend.features.computed_parameters.view as computed_view


class DummyContainer:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_computed_parameters_view_starts_simulation_directly(monkeypatch):
    clicked_buttons = []
    calls = {
        "simulation_started": False,
        "overlay_messages": [],
        "markup": [],
        "rerun": False,
    }

    @contextmanager
    def fake_global_loading(message, **kwargs):
        calls["overlay_messages"].append((message, kwargs))
        yield

    fake_streamlit = SimpleNamespace(
        session_state={
            "backend_state": {
                "simulation_plan": {"evaluation_metrics": []},
                "computed_parameters": {"time_limit": {"value": 120}},
            }
        },
        container=lambda **kwargs: DummyContainer(),
        markdown=lambda body, *args, **kwargs: calls["markup"].append(body),
        dataframe=lambda *args, **kwargs: None,
        info=lambda *args, **kwargs: None,
        button=lambda label, **kwargs: clicked_buttons.append((label, kwargs))
        or kwargs["on_click"]()
        or False,
        rerun=lambda: calls.update(rerun=True),
    )

    monkeypatch.setattr(computed_view, "st", fake_streamlit)
    monkeypatch.setattr(computed_view, "render_page_header", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        computed_view,
        "render_simulation_plan_review",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        computed_view,
        "global_loading",
        fake_global_loading,
    )
    monkeypatch.setattr(
        computed_view,
        "run_simulation_from_plan",
        lambda **kwargs: calls.update(
            simulation_started=True,
            simulation_kwargs=kwargs,
        ),
    )

    computed_view.render_simulation_plan_view()

    assert clicked_buttons[0][0] == "Simulation starten"
    assert "cogsim-plan-intro" in "".join(calls["markup"])
    assert "cogsim-plan-value-grid" in "".join(calls["markup"])
    assert fake_streamlit.session_state["pending_simulation_run"] is True
    assert calls["simulation_started"] is False
    assert calls["overlay_messages"] == []


def test_computed_parameters_view_runs_pending_simulation_without_rendering_plan(
    monkeypatch,
):
    calls = {
        "simulation_started": False,
        "overlay_messages": [],
        "markup": [],
        "rerun": False,
    }

    @contextmanager
    def fake_global_loading(message, **kwargs):
        calls["overlay_messages"].append((message, kwargs))
        yield

    fake_streamlit = SimpleNamespace(
        session_state={
            "pending_simulation_run": True,
            "backend_state": {
                "simulation_plan": {"evaluation_metrics": []},
                "computed_parameters": {"time_limit": {"value": 120}},
            },
        },
        container=lambda **kwargs: DummyContainer(),
        markdown=lambda body, *args, **kwargs: calls["markup"].append(body),
        dataframe=lambda *args, **kwargs: None,
        info=lambda *args, **kwargs: None,
        button=lambda *args, **kwargs: None,
        rerun=lambda: calls.update(rerun=True),
    )

    monkeypatch.setattr(computed_view, "st", fake_streamlit)
    monkeypatch.setattr(computed_view, "render_page_header", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        computed_view,
        "render_simulation_plan_review",
        lambda *args, **kwargs: calls.update(plan_rendered=True),
    )
    monkeypatch.setattr(
        computed_view,
        "global_loading",
        fake_global_loading,
    )
    monkeypatch.setattr(
        computed_view,
        "run_simulation_from_plan",
        lambda **kwargs: calls.update(
            simulation_started=True,
            simulation_kwargs=kwargs,
        ),
    )

    computed_view.render_simulation_plan_view()

    assert calls["simulation_started"] is True
    assert calls["simulation_kwargs"] == {"rerun": False}
    assert calls["rerun"] is True
    assert calls.get("plan_rendered") is None
    assert calls["markup"] == []
    assert calls["overlay_messages"] == [
        (
            "Die Simulation wird ausgeführt.",
            {
                "hint": (
                    "Die ausgewählten Profile werden mit denselben Grundlagen verglichen."
                ),
                "min_visible_seconds": 7.0,
                "estimated_seconds": 7.0,
            },
        )
    ]


def test_computed_parameter_rows_hide_assumptions():
    rows = computed_view.build_computed_parameter_rows(
        {
            "time_limit": {"value": 120},
            "assumptions": ["Technische Annahme"],
        }
    )

    assert rows == [{"Parameter": "Time Limit", "Wert": 120}]
