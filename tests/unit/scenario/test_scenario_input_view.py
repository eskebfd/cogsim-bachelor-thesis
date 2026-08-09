from contextlib import contextmanager
from types import SimpleNamespace

import frontend.features.scenario.input_section as input_section
import frontend.features.scenario.scenario_form as scenario_form
import frontend.features.scenario.screenshot_tool as screenshot_tool
import frontend.features.scenario.view as scenario_view


class FakeSessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc

    def __setattr__(self, key, value):
        self[key] = value


class DummyContainer:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def fake_input_section_streamlit(session_state):
    return SimpleNamespace(
        session_state=session_state,
        container=lambda **kwargs: DummyContainer(),
        markdown=lambda *args, **kwargs: None,
        expander=lambda *args, **kwargs: DummyContainer(),
        warning=lambda *args, **kwargs: None,
    )


def test_scenario_input_renders_text_section(monkeypatch):
    session_state = FakeSessionState()
    calls = {"text": 0}

    monkeypatch.setattr(
        input_section,
        "st",
        fake_input_section_streamlit(session_state),
    )
    monkeypatch.setattr(
        input_section,
        "_render_scenario_text_input",
        lambda: calls.update(text=calls["text"] + 1) or "Beschreibung",
    )

    result = input_section.render_scenario_input_section()

    assert result == "Beschreibung"
    assert calls == {"text": 1}


def test_scenario_text_state_survives_mode_switch(monkeypatch):
    session_state = FakeSessionState(
        {
            "scenario_task": "Hotel auswählen",
            "scenario_interface": "Suchformular und Ergebnisliste",
            "scenario_environment": "Unterwegs mit Zeitdruck",
        }
    )
    monkeypatch.setattr(
        scenario_form,
        "st",
        SimpleNamespace(session_state=session_state),
    )

    description = scenario_form.build_scenario_description()

    assert "Hotel auswählen" in description
    assert "Suchformular und Ergebnisliste" in description
    assert "Unterwegs mit Zeitdruck" in description


def test_task_text_area_height_grows_with_content():
    short_height = scenario_form._dynamic_task_text_area_height("Kurze Aufgabe")
    long_height = scenario_form._dynamic_task_text_area_height(
        "\n".join(
            [
                "Aus dem Screenshot abgeleiteter Aufgabenablauf:",
                "Ziel: Hotel buchen",
                "Hauptaufgabe: Unterkunft auswählen",
                "Mögliche Arbeitsschritte:",
                "1. Suchergebnisse prüfen",
                "2. Filter anwenden",
                "3. Hotel vergleichen",
                "4. Details lesen",
                "5. Verfügbarkeit prüfen",
                "6. Buchung starten",
            ]
        )
    )

    assert short_height >= 120
    assert long_height > short_height


def test_screenshot_analysis_fills_empty_task_and_interface_fields(monkeypatch):
    session_state = FakeSessionState(
        {
            "scenario_task": "",
            "scenario_interface": "",
            "screenshot_task_analysis_applied_key": None,
        }
    )
    analysis = {
        "user_goal": "Passende Unterkunft finden",
        "main_task": "Hotel auswählen",
        "interface_description": "Die Oberfläche zeigt Hotelkarten mit Preisen und Bewertungen.",
        "visible_elements": ["Suchfeld", "Filter", "Hotelkarten"],
        "hta_steps": [
            {
                "number": "1",
                "title": "Suchergebnisse prüfen",
                "description": "Die angezeigten Angebote vergleichen.",
            },
            {
                "number": "2",
                "title": "Hotel auswählen",
                "description": "",
            },
        ],
    }
    image_key = ("screen.png", "image/png", 123, "abc", "xyz")

    monkeypatch.setattr(
        screenshot_tool,
        "st",
        SimpleNamespace(session_state=session_state),
    )

    screenshot_tool._apply_screenshot_analysis_to_task_field(
        analysis,
        image_key,
    )

    assert "Aus dem Screenshot abgeleiteter Aufgabenablauf" in (
        session_state["screenshot_task_analysis_pending_text"]
    )
    assert "1. Suchergebnisse prüfen" in (
        session_state["screenshot_task_analysis_pending_text"]
    )
    assert "Hotelkarten" in (
        session_state["screenshot_interface_analysis_pending_text"]
    )
    assert session_state["screenshot_task_analysis_applied_key"] == image_key


def test_screenshot_analysis_preserves_existing_user_text(monkeypatch):
    session_state = FakeSessionState(
        {
            "scenario_task": "Eigene Aufgabe",
            "scenario_interface": "Eigenes Interface",
            "screenshot_task_analysis_applied_key": None,
        }
    )
    image_key = ("screen.png", "image/png", 123, "abc", "xyz")

    monkeypatch.setattr(
        screenshot_tool,
        "st",
        SimpleNamespace(session_state=session_state),
    )

    screenshot_tool._apply_screenshot_analysis_to_task_field(
        {
            "main_task": "Hotel auswählen",
            "interface_description": "Die Oberfläche zeigt Hotelkarten.",
        },
        image_key,
    )

    assert session_state["scenario_task"] == "Eigene Aufgabe"
    assert session_state["scenario_interface"] == "Eigenes Interface"
    assert session_state.get("screenshot_task_analysis_pending_text") is None
    assert session_state.get("screenshot_interface_analysis_pending_text") is None


def test_pending_screenshot_analysis_is_applied_before_task_widget(monkeypatch):
    session_state = FakeSessionState(
        {
            "scenario_task": "Hotel in Berlin buchen",
            "scenario_interface": "",
            "screenshot_task_analysis_pending_text": (
                "Hotel in Berlin buchen\n\n"
                "Aus dem Screenshot abgeleiteter Aufgabenablauf:\n"
                "1. Suchergebnisse prüfen"
            ),
            "screenshot_interface_analysis_pending_text": (
                "Die Oberfläche zeigt Hotelkarten."
            ),
        }
    )

    monkeypatch.setattr(
        screenshot_tool,
        "st",
        SimpleNamespace(session_state=session_state),
    )

    screenshot_tool.apply_pending_screenshot_task_text()

    assert "Aus dem Screenshot abgeleiteter Aufgabenablauf" in (
        session_state["scenario_task"]
    )
    assert session_state["scenario_interface"] == "Die Oberfläche zeigt Hotelkarten."
    assert session_state["screenshot_task_analysis_pending_text"] is None
    assert session_state["screenshot_interface_analysis_pending_text"] is None


def test_screenshot_analysis_is_not_added_twice(monkeypatch):
    image_key = ("screen.png", "image/png", 123, "abc", "xyz")
    session_state = FakeSessionState(
        {
            "scenario_task": "",
            "screenshot_task_analysis_applied_key": image_key,
        }
    )

    monkeypatch.setattr(
        screenshot_tool,
        "st",
        SimpleNamespace(session_state=session_state),
    )

    screenshot_tool._apply_screenshot_analysis_to_task_field(
        {
            "main_task": "Hotel auswählen",
            "hta_steps": [{"number": "1", "title": "Hotel prüfen"}],
        },
        image_key,
    )

    assert session_state["scenario_task"] == ""


def fake_view_streamlit(session_state, *, button_clicked=True):
    errors = []
    warnings = []
    return SimpleNamespace(
        session_state=session_state,
        write=lambda *args, **kwargs: None,
        button=lambda *args, **kwargs: button_clicked,
        error=lambda message: errors.append(message),
        warning=lambda message: warnings.append(message),
        _errors=errors,
        _warnings=warnings,
    )


def test_scenario_analysis_uses_hidden_uploaded_screenshot(monkeypatch):
    screenshot = {"filename": "screen.png"}
    session_state = FakeSessionState(
        {
            "scenario_input": "Aufgabe\nHotel suchen",
            "scenario_task": "Hotel suchen",
            "scenario_interface": "",
            "scenario_environment": "",
            "scenario_image_upload": screenshot,
        }
    )
    fake_st = fake_view_streamlit(session_state)
    captured = {}
    monkeypatch.setattr(scenario_view, "st", fake_st)
    monkeypatch.setattr(
        scenario_view,
        "render_page_header",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        scenario_view,
        "render_scenario_input_section",
        lambda: session_state["scenario_input"],
    )
    monkeypatch.setattr(
        scenario_view,
        "update_backend_state",
        lambda **kwargs: captured.update(backend_state=kwargs),
    )
    monkeypatch.setattr(
        scenario_view,
        "reset_generated_data",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        scenario_view,
        "generate_task_flow_with_progress",
        lambda description: captured.update(task_flow_description=description)
        or True,
    )
    monkeypatch.setattr(scenario_view, "go_to_step", lambda step: captured.update(step=step))
    monkeypatch.setattr(scenario_view, "get_session_id", lambda: "session-1")
    monkeypatch.setattr(
        scenario_view,
        "render_multimodal_summary",
        lambda *args, **kwargs: None,
    )

    scenario_view.render_scenario_input_view()

    assert captured["backend_state"]["scenario_image"] == screenshot
    assert captured["task_flow_description"] == "Aufgabe\nHotel suchen"
    assert captured["step"] == 4


def test_empty_scenario_without_screenshot_does_not_start_analysis(monkeypatch):
    session_state = FakeSessionState(
        {
            "scenario_input": "Aufgabe\n\nInterface\n\nUmgebung\n",
            "scenario_task": "",
            "scenario_interface": "",
            "scenario_environment": "",
            "scenario_image_upload": None,
        }
    )
    fake_st = fake_view_streamlit(session_state)
    calls = {"analysis": 0}

    monkeypatch.setattr(scenario_view, "st", fake_st)
    monkeypatch.setattr(
        scenario_view,
        "render_page_header",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        scenario_view,
        "render_scenario_input_section",
        lambda: session_state["scenario_input"],
    )
    monkeypatch.setattr(
        scenario_view,
        "update_backend_state",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        scenario_view,
        "generate_task_flow_with_progress",
        lambda *args, **kwargs: calls.update(analysis=calls["analysis"] + 1),
    )
    monkeypatch.setattr(
        scenario_view,
        "render_multimodal_summary",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(scenario_view, "get_session_id", lambda: "session-1")

    scenario_view.render_scenario_input_view()

    assert calls["analysis"] == 0
    assert fake_st._errors


def test_uploaded_screenshot_card_renders_compact_thumbnail(monkeypatch):
    rendered_html = []
    image_calls = []
    button_calls = []

    fake_st = SimpleNamespace(
        container=lambda **kwargs: DummyContainer(),
        columns=lambda *args, **kwargs: [
            DummyContainer(),
            DummyContainer(),
            DummyContainer(),
        ],
        markdown=lambda body, **kwargs: rendered_html.append(body),
        button=lambda *args, **kwargs: button_calls.append((args, kwargs)),
        image=lambda *args, **kwargs: image_calls.append((args, kwargs)),
    )
    payload = {
        "filename": "screen.png",
        "mime_type": "image/png",
        "size_bytes": 2048,
        "data_base64": "ZmFrZS1pbWFnZQ==",
    }

    monkeypatch.setattr(screenshot_tool, "st", fake_st)

    screenshot_tool._render_uploaded_image_card(payload)

    joined_html = "\n".join(rendered_html)
    assert "cogsim-uploaded-image__thumbnail" in joined_html
    assert "data:image/png;base64,ZmFrZS1pbWFnZQ==" in joined_html
    assert "Screenshot hinzugefügt" in joined_html
    assert "screen.png" in joined_html
    assert button_calls
    assert image_calls == []


def test_existing_screenshot_hides_file_uploader(monkeypatch):
    rendered_cards = []
    session_state = FakeSessionState(
        {
            "scenario_image_upload": {
                "filename": "screen.png",
                "mime_type": "image/png",
                "size_bytes": 2048,
                "data_base64": "ZmFrZS1pbWFnZQ==",
            },
            "screenshot_task_analysis": {"user_goal": "Hotel finden"},
            "screenshot_task_analysis_error": None,
        }
    )
    fake_st = SimpleNamespace(
        session_state=session_state,
        markdown=lambda *args, **kwargs: None,
        file_uploader=lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("file uploader should not render for existing upload")
        ),
    )

    monkeypatch.setattr(screenshot_tool, "st", fake_st)
    monkeypatch.setattr(
        screenshot_tool,
        "_render_uploaded_image_card",
        lambda payload: rendered_cards.append(payload),
    )

    screenshot_tool._render_screenshot_upload()

    assert rendered_cards == [session_state["scenario_image_upload"]]


def test_new_screenshot_upload_starts_analysis_automatically(monkeypatch):
    class UploadedFile:
        name = "screen.png"
        type = "image/png"

        def getvalue(self):
            return b"fake-image"

    session_state = FakeSessionState(
        {
            "scenario_image_uploader_version": 0,
            "scenario_image_upload": None,
            "screenshot_task_analysis": None,
            "screenshot_task_analysis_error": None,
            "screenshot_task_analysis_image_key": None,
        }
    )
    overlay_messages = []
    analysis_calls = []
    rendered_cards = []
    rerun_calls = []

    @contextmanager
    def fake_global_loading(message, **kwargs):
        overlay_messages.append((message, kwargs))
        yield

    fake_st = SimpleNamespace(
        session_state=session_state,
        markdown=lambda *args, **kwargs: None,
        file_uploader=lambda *args, **kwargs: UploadedFile(),
        rerun=lambda: rerun_calls.append(True),
    )

    monkeypatch.setattr(screenshot_tool, "st", fake_st)
    monkeypatch.setattr(screenshot_tool, "global_loading", fake_global_loading)
    monkeypatch.setattr(screenshot_tool, "get_session_id", lambda: "session-1")
    monkeypatch.setattr(
        screenshot_tool,
        "analyze_screenshot_task_structure",
        lambda payload, session_id=None: analysis_calls.append(
            (payload, session_id)
        )
        or {"screenshot_task_analysis": {"user_goal": "Hotel finden"}},
    )
    monkeypatch.setattr(
        screenshot_tool,
        "_render_uploaded_image_card",
        lambda payload: rendered_cards.append(payload),
    )

    screenshot_tool._render_screenshot_upload()

    assert session_state["scenario_image_upload"]["filename"] == "screen.png"
    assert analysis_calls[0][1] == "session-1"
    assert session_state["screenshot_task_analysis"] == {
        "user_goal": "Hotel finden"
    }
    assert overlay_messages[0][0] == (
        "Screenshot wird auf erkannte Hinweise analysiert."
    )
    assert rerun_calls == [True]
