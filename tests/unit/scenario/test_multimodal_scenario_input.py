import base64
from io import BytesIO

import pytest
from PIL import Image

from backend.workflow.nodes.scenario_nodes import extract_dimensions
from backend.domains.scenario.schemas.multimodal import (
    ScenarioImageAnalysis,
    ScenarioImageMetadata,
    ScreenshotTaskAnalysis,
    VisualSignal,
)
from backend.api.routes import execute_workflow_command
from backend.transport.schemas.workflow import AnalyzeScreenshotCommand
from backend.core.llm import client as llm_service
from backend.workflow.routing import update_state_router
from backend.domains.scenario.services.multimodal_analysis import (
    fuse_text_and_image_dimensions,
)
from backend.domains.scenario.services.image_processing import (
    MAX_SCENARIO_IMAGE_BYTES,
    ScenarioImageValidationError,
    decode_scenario_image,
)
from frontend.features.scenario.screenshot_tool import (
    build_screenshot_analysis_image_key,
    build_scenario_image_payload,
)
from frontend.shared.services.workflow_payloads import (
    build_analyze_dimensions_payload,
    build_analyze_screenshot_payload,
)
from tests.fixtures.frontend_mock_data import MOCK_DIMENSIONS


def png_bytes() -> bytes:
    image = Image.new("RGB", (2, 2), color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


class UploadedFile:
    def __init__(self, data: bytes, *, name: str = "screen.png", mime: str = "image/png"):
        self.name = name
        self.type = mime
        self._data = data

    def getvalue(self) -> bytes:
        return self._data


def image_payload(data: bytes | None = None, *, mime: str = "image/png") -> dict:
    data = data if data is not None else png_bytes()
    return {
        "filename": "screen.png",
        "mime_type": mime,
        "size_bytes": len(data),
        "data_base64": base64.b64encode(data).decode("ascii"),
    }


def dimensions():
    return llm_service.ScenarioDimensionsSchema.model_validate(MOCK_DIMENSIONS)


def test_text_only_workflow_does_not_run_image_analysis(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "invoke_structured",
        lambda *args, **kwargs: dimensions(),
    )
    monkeypatch.setattr(
        llm_service,
        "analyze_scenario_image",
        lambda *args, **kwargs: pytest.fail("image analysis must not run"),
    )

    result = llm_service.extract_scenario_dimensions("Online-Formular ausfüllen")

    assert result.scenario_summary
    assert result.scenario_image_metadata is None


def test_text_dimensions_are_composed_from_split_dimension_parts(monkeypatch):
    source_dimensions = dimensions()
    calls = []

    def fake_context(scenario_description):
        calls.append("context")
        return llm_service.ScenarioDimensionContextSchema.model_validate(
            source_dimensions.model_dump()
        )

    def fake_task(scenario_description, dimension_context):
        calls.append("task")
        return source_dimensions.task_signals

    def fake_interface(scenario_description, dimension_context):
        calls.append("interface")
        return source_dimensions.interface_signals

    def fake_environment(scenario_description, dimension_context):
        calls.append("environment")
        return source_dimensions.environment_signals

    monkeypatch.setattr(
        llm_service,
        "extract_scenario_dimension_context",
        fake_context,
    )
    monkeypatch.setattr(
        llm_service,
        "extract_task_dimension_signals",
        fake_task,
    )
    monkeypatch.setattr(
        llm_service,
        "extract_interface_dimension_signals",
        fake_interface,
    )
    monkeypatch.setattr(
        llm_service,
        "extract_environment_dimension_signals",
        fake_environment,
    )
    monkeypatch.setattr(
        llm_service,
        "analyze_scenario_image",
        lambda *args, **kwargs: pytest.fail("image analysis must not run"),
    )

    result = llm_service.extract_scenario_dimensions("Online-Formular ausfüllen")

    assert result.scenario_summary == source_dimensions.scenario_summary
    assert result.task_signals.task_complexity.value == (
        source_dimensions.task_signals.task_complexity.value
    )
    assert result.interface_signals.visual_clutter.value == (
        source_dimensions.interface_signals.visual_clutter.value
    )
    assert result.environment_signals.time_pressure.value == (
        source_dimensions.environment_signals.time_pressure.value
    )
    assert calls[0] == "context"
    assert sorted(calls[1:]) == ["environment", "interface", "task"]


def test_dimension_workflow_routes_text_to_parallel_fanout_and_images_to_fallback():
    assert update_state_router(
        {
            "current_stage": "dimensions",
            "scenario_description": "Online-Formular ausfüllen",
        }
    ) == "extract_dimension_context"

    assert update_state_router(
        {
            "current_stage": "dimensions",
            "scenario_description": "Online-Formular ausfüllen",
            "scenario_image": {"filename": "screen.png"},
        }
    ) == "extract_dimensions"


def test_text_plus_valid_image_is_accepted_and_fused(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "invoke_structured",
        lambda *args, **kwargs: dimensions(),
    )
    monkeypatch.setattr(
        llm_service,
        "analyze_scenario_image",
        lambda **kwargs: ScenarioImageAnalysis(
            image_signals=["Viele sichtbare Textblöcke"],
            confirmed_signals=["Hohe Textmenge"],
            interface_signals={
                "text_volume": VisualSignal(
                    value=50,
                    confidence="high",
                    evidence_text="Mehrere Textblöcke sichtbar.",
                )
            },
        ),
    )

    result = llm_service.extract_scenario_dimensions(
        "Die Website enthält viele lange Hinweise.",
        image_payload(),
    )

    assert result.scenario_image_metadata is not None
    assert result.interface_signals.text_volume.source in {"image", "text_and_image"}
    assert "Hohe Textmenge" in result.multimodal_analysis.confirmed_signals


def test_image_only_creates_restricted_state(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "analyze_scenario_image",
        lambda **kwargs: ScenarioImageAnalysis(
            image_signals=["Formular mit mehreren Feldern sichtbar"],
            missing_information=["Nutzungskontext fehlt"],
            interface_signals={
                "visual_clutter": VisualSignal(
                    value=70,
                    confidence="high",
                    evidence_text="Viele sichtbare Elemente.",
                )
            },
        ),
    )

    result = llm_service.extract_scenario_dimensions("", image_payload())

    assert "beschränkt" in result.scenario_summary.lower()
    assert "Nutzungskontext fehlt" in result.multimodal_analysis.missing_information
    assert result.user_model if hasattr(result, "user_model") else True


def test_invalid_image_format_is_rejected():
    with pytest.raises(ScenarioImageValidationError, match="Unsupported"):
        decode_scenario_image(image_payload(mime="image/gif"))


def test_too_large_image_is_rejected():
    data = b"x" * (MAX_SCENARIO_IMAGE_BYTES + 1)
    with pytest.raises(ScenarioImageValidationError, match="too large"):
        decode_scenario_image(image_payload(data))


def test_damaged_image_is_rejected():
    with pytest.raises(ScenarioImageValidationError, match="damaged"):
        decode_scenario_image(image_payload(b"not an image"))


def test_uncertain_image_information_is_not_treated_as_fact():
    text_dimensions = dimensions()
    fused = fuse_text_and_image_dimensions(
        text_dimensions,
        ScenarioImageAnalysis(
            interface_signals={
                "visual_clutter": VisualSignal(
                    value=95,
                    confidence="low",
                    uncertainty_notes=["Nicht sicher erkennbar."],
                )
            }
        ),
        image_metadata=ScenarioImageMetadata(
            filename="screen.png",
            mime_type="image/png",
            size_bytes=10,
        ),
    )

    assert fused.interface_signals.visual_clutter.source == "text"
    assert any(
        "nicht als sicherer Faktenwert" in note
        for note in fused.interface_signals.visual_clutter.uncertainty_notes
    )


def test_conflicting_text_and_image_signals_are_marked():
    text_dimensions = dimensions()
    text_dimensions.interface_signals.visual_clutter.value = 10
    fused = fuse_text_and_image_dimensions(
        text_dimensions,
        ScenarioImageAnalysis(
            interface_signals={
                "visual_clutter": VisualSignal(
                    value=90,
                    confidence="high",
                    evidence_text="Viele konkurrierende Elemente.",
                )
            }
        ),
    )

    assert fused.interface_signals.visual_clutter.value == 10
    assert fused.multimodal_analysis.conflicts


def test_image_analysis_failure_falls_back_to_text(monkeypatch):
    monkeypatch.setattr(
        llm_service,
        "invoke_structured",
        lambda *args, **kwargs: dimensions(),
    )
    monkeypatch.setattr(
        llm_service,
        "analyze_scenario_image",
        lambda **kwargs: (_ for _ in ()).throw(RuntimeError("vision unavailable")),
    )

    result = llm_service.extract_scenario_dimensions("Text reicht aus.", image_payload())

    assert result.scenario_summary
    assert result.multimodal_analysis.image_analysis_failed is True
    assert "vision unavailable" in result.multimodal_analysis.image_analysis_warning


def test_frontend_payload_contains_text_and_image():
    payload = build_analyze_dimensions_payload(
        "Test scenario",
        scenario_image={"filename": "screen.png"},
    )

    assert payload["scenario_text"] == "Test scenario"
    assert payload["scenario_image"] == {"filename": "screen.png"}


def test_frontend_screenshot_payload_contains_only_image():
    payload = build_analyze_screenshot_payload({"filename": "screen.png"})

    assert payload == {"scenario_image": {"filename": "screen.png"}}


def test_screenshot_analysis_image_key_changes_when_image_changes():
    first = image_payload(b"first image")
    second = image_payload(b"second image")

    assert build_screenshot_analysis_image_key(first) != (
        build_screenshot_analysis_image_key(second)
    )


def test_screenshot_task_analysis_schema_supports_hta_hypotheses():
    analysis = ScreenshotTaskAnalysis.model_validate(
        {
            "user_goal": "Eine Unterkunft auswählen.",
            "main_task": "Hotelangebot prüfen.",
            "task_description": "Die Person prüft sichtbare Angebote.",
            "interface_description": "Die Oberfläche zeigt eine Ergebnisliste mit Hotelkarten.",
            "hta_steps": [
                {
                    "number": "1",
                    "title": "Ergebnisliste prüfen",
                    "description": "Sichtbare Angebote vergleichen.",
                    "subtasks": ["Preis lesen", "Bewertung prüfen"],
                    "interface_elements": ["Ergebnisliste", "Preisangabe"],
                    "confidence": 0.82,
                }
            ],
            "decision_points": ["Passt das Angebot zum Budget?"],
            "interface_elements": ["Suchfeld", "Filter"],
            "visible_elements": ["Hotelkarte", "Preis", "Bewertung"],
            "uncertainties": ["Nicht sichtbare Detailseite."],
            "missing_information": ["Nicht sichtbare Folgeschritte."],
            "warning": None,
        }
    )

    assert analysis.hta_steps[0].title == "Ergebnisliste prüfen"
    assert analysis.hta_steps[0].confidence == pytest.approx(0.82)
    assert analysis.task_description == "Die Person prüft sichtbare Angebote."
    assert "Hotelkarten" in analysis.interface_description


def test_screenshot_task_structure_uses_existing_image_decoder(monkeypatch):
    captured = {}

    def fake_analysis(**kwargs):
        captured["metadata"] = kwargs["metadata"]
        return ScreenshotTaskAnalysis(
            user_goal="Unterkunft auswählen",
            main_task="Angebot prüfen",
            interface_description="Die Oberfläche zeigt Hotelkarten.",
        )

    monkeypatch.setattr(
        llm_service,
        "analyze_screenshot_for_task_structure",
        fake_analysis,
    )

    result = llm_service.analyze_screenshot_task_structure(image_payload())

    assert result.user_goal == "Unterkunft auswählen"
    assert result.interface_description == "Die Oberfläche zeigt Hotelkarten."
    assert captured["metadata"].filename == "screen.png"


def test_analyze_screenshot_command_returns_structured_result(monkeypatch):
    monkeypatch.setattr(
        "backend.api.routes.analyze_screenshot_task_structure",
        lambda scenario_image: ScreenshotTaskAnalysis(
            user_goal="Unterkunft auswählen",
            main_task="Hotel prüfen",
            interface_description="Die Oberfläche zeigt Filter.",
        ),
    )

    response = execute_workflow_command(
        AnalyzeScreenshotCommand(
            session_id="session-1",
            command="analyze_screenshot",
            payload={"scenario_image": image_payload()},
        )
    )

    assert response["session_id"] == "session-1"
    assert response["current_stage"] == "scenario_screenshot_analysis"
    assert response["screenshot_task_analysis"]["main_task"] == "Hotel prüfen"
    assert response["screenshot_task_analysis"]["interface_description"] == (
        "Die Oberfläche zeigt Filter."
    )


def test_frontend_image_payload_builder_accepts_png(monkeypatch):
    payload = build_scenario_image_payload(UploadedFile(png_bytes()))

    assert payload["mime_type"] == "image/png"
    assert payload["data_base64"]


def test_dimension_node_drops_raw_image_from_result(monkeypatch):
    monkeypatch.setattr(
        "backend.workflow.nodes.scenario_nodes.analyze_scenario_dimensions",
        lambda description, scenario_image=None: dimensions(),
    )

    result = extract_dimensions(
        {
            "current_stage": "dimensions",
            "scenario_description": "Test",
            "scenario_context": {},
            "scenario_image": image_payload(),
        }
    )

    assert result["scenario_image"] is None
