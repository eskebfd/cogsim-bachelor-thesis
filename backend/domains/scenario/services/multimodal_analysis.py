import base64

from langchain_core.messages import HumanMessage

from backend.domains.scenario.schemas.multimodal import (
    MultimodalAnalysis,
    ScenarioImageAnalysis,
    ScenarioImageMetadata,
    ScreenshotTaskAnalysis,
    VisualSignal,
)
from backend.domains.scenario.schemas.dimensions import (
    ScenarioAttributeSignalSchema,
    ScenarioDimensionsSchema,
)
from backend.core.llm.prompt_loader import load_prompt
from backend.core.logging.workflow_logging import log_duration, logger


IMAGE_SUPPORTED_INTERFACE_ATTRIBUTES = {
    "text_volume",
    "sentence_length",
    "word_difficulty",
    "technical_terms",
    "visual_clutter",
    "navigation_complexity",
    "accessibility_support",
    "feedback_quality",
    "text_legibility",
    "text_density",
    "line_tracking_difficulty",
    "stimulus_density",
    "irrelevant_signal_load",
    "feedback_interruptiveness",
    "focus_guidance",
}
IMAGE_SUPPORTED_TASK_ATTRIBUTES = {
    "task_complexity",
    "number_of_steps",
    "reading_demand",
    "input_demand",
    "unfamiliar_word_density",
    "orthographic_irregularity",
    "morphological_complexity",
    "sustained_attention_demand",
    "task_switching_demand",
    "inhibition_demand",
    "divided_attention_demand",
}


def _merge_lists(*values: list[str]) -> list[str]:
    merged = []
    for group in values:
        for item in group:
            if item and item not in merged:
                merged.append(item)
    return merged


def _fallback_signal(value: int | None, evidence_text: str) -> VisualSignal:
    return VisualSignal(
        value=value,
        confidence="low" if value is not None else "unknown",
        evidence_text=evidence_text,
        uncertainty_notes=[
            "Dieser Wert stammt aus einer heuristischen Fallback-Analyse und ist unsicher."
        ],
    )


def build_fallback_image_analysis(
    metadata: ScenarioImageMetadata,
    warning: str | None = None,
) -> ScenarioImageAnalysis:
    assumptions = [
        "Ohne erfolgreiche multimodale LLM-Analyse werden nur technische Bildmetadaten verwendet."
    ]
    if warning:
        assumptions.append(warning)
    area = (metadata.width or 0) * (metadata.height or 0)
    clutter_estimate = 55 if area >= 1_000_000 else 45 if area else None
    return ScenarioImageAnalysis(
        image_signals=[
            f"Bild '{metadata.filename}' wurde mit {metadata.width}x{metadata.height}px hochgeladen."
            if metadata.width and metadata.height
            else f"Bild '{metadata.filename}' wurde hochgeladen."
        ],
        assumptions=assumptions,
        missing_information=[
            "Nutzungskontext, Umgebungsbedingungen und konkrete Handlungsziele sind aus einem Screenshot allein nicht zuverlässig ableitbar."
        ],
        confidence_notes=[
            "Fallback ohne externe Bildanalyse; visuelle Signale sind entsprechend unsicher."
        ],
        interface_signals={
            "visual_clutter": _fallback_signal(
                clutter_estimate,
                "Grobe Schätzung aus Bildauflösung, nicht aus semantischer UI-Erkennung.",
            )
        },
    )


def analyze_scenario_image(
    *,
    image_bytes: bytes,
    metadata: ScenarioImageMetadata,
    scenario_text: str | None,
    structured_image_model,
) -> ScenarioImageAnalysis:
    prompt = load_prompt("scenario_image_analysis.prompt.txt").format(
        scenario_text=scenario_text or "[kein Szenariotext]"
    )
    image_data = base64.b64encode(image_bytes).decode("ascii")
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{metadata.mime_type};base64,{image_data}"
                },
            },
        ]
    )

    with log_duration(
        "llm.analyze_scenario_image",
        image_bytes=len(image_bytes),
        scenario_text_chars=len(scenario_text or ""),
    ):
        result = structured_image_model.invoke([message])

    if isinstance(result, dict) and "parsed" in result:
        parsed = result.get("parsed")
        if parsed is None:
            raise ValueError("LLM returned no parsed image analysis.")
        return parsed
    return ScenarioImageAnalysis.model_validate(result)


def analyze_screenshot_for_task_structure(
    *,
    image_bytes: bytes,
    metadata: ScenarioImageMetadata,
    structured_task_analysis_model,
) -> ScreenshotTaskAnalysis:
    prompt = load_prompt("screenshot_task_structure.prompt.txt")
    image_data = base64.b64encode(image_bytes).decode("ascii")
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{metadata.mime_type};base64,{image_data}"
                },
            },
        ]
    )

    with log_duration(
        "llm.analyze_screenshot_task_structure",
        image_bytes=len(image_bytes),
    ):
        result = structured_task_analysis_model.invoke([message])

    if isinstance(result, dict) and "parsed" in result:
        parsed = result.get("parsed")
        if parsed is None:
            raise ValueError("LLM returned no parsed screenshot task analysis.")
        return parsed
    return ScreenshotTaskAnalysis.model_validate(result)


def _signal_is_usable(signal: VisualSignal) -> bool:
    return signal.value is not None and signal.confidence in {"medium", "high"}


def _apply_visual_signal(
    text_signal: ScenarioAttributeSignalSchema,
    image_signal: VisualSignal,
    *,
    conflicts: list[str],
) -> ScenarioAttributeSignalSchema:
    if not _signal_is_usable(image_signal):
        updated = text_signal.model_copy(deep=True)
        updated.uncertainty_notes = _merge_lists(
            updated.uncertainty_notes,
            image_signal.uncertainty_notes,
            [
                "Bildinformation wurde nicht als sicherer Faktenwert übernommen."
            ],
        )
        return updated

    difference = abs(text_signal.value - int(image_signal.value))
    if difference >= 30:
        conflicts.append(
            f"{text_signal.name}: Textwert {text_signal.value} widerspricht Bildwert {image_signal.value}."
        )
        source = "text"
        value = text_signal.value
    elif difference <= 15:
        source = "text_and_image"
        value = round((text_signal.value + int(image_signal.value)) / 2)
    else:
        source = "image"
        value = int(image_signal.value)

    updated = text_signal.model_copy(deep=True)
    updated.value = value
    updated.source = source
    updated.evidence_text = image_signal.evidence_text or text_signal.evidence_text
    updated.uncertainty_notes = _merge_lists(
        updated.uncertainty_notes,
        image_signal.uncertainty_notes,
    )
    return updated


def fuse_text_and_image_dimensions(
    dimensions: ScenarioDimensionsSchema,
    image_analysis: ScenarioImageAnalysis | None,
    *,
    image_metadata: ScenarioImageMetadata | None = None,
    image_analysis_failed: bool = False,
    image_analysis_warning: str | None = None,
) -> ScenarioDimensionsSchema:
    if image_analysis is None:
        updated = dimensions.model_copy(deep=True)
        updated.scenario_image_metadata = image_metadata
        updated.multimodal_analysis = MultimodalAnalysis(
            text_signals=["Szenariodimensionen wurden aus dem Text abgeleitet."],
            missing_information=[],
            image_analysis_failed=image_analysis_failed,
            image_analysis_warning=image_analysis_warning,
        )
        return updated

    updated = dimensions.model_copy(deep=True)
    conflicts: list[str] = []
    for attribute_id, image_signal in image_analysis.interface_signals.items():
        if attribute_id not in IMAGE_SUPPORTED_INTERFACE_ATTRIBUTES:
            continue
        current = getattr(updated.interface_signals, attribute_id, None)
        if current is not None:
            setattr(
                updated.interface_signals,
                attribute_id,
                _apply_visual_signal(current, image_signal, conflicts=conflicts),
            )

    for attribute_id, image_signal in image_analysis.task_signals.items():
        if attribute_id not in IMAGE_SUPPORTED_TASK_ATTRIBUTES:
            continue
        current = getattr(updated.task_signals, attribute_id, None)
        if current is not None:
            setattr(
                updated.task_signals,
                attribute_id,
                _apply_visual_signal(current, image_signal, conflicts=conflicts),
            )

    updated.scenario_image_metadata = image_metadata
    updated.multimodal_analysis = MultimodalAnalysis(
        text_signals=image_analysis.text_signals
        or ["Szenariodimensionen wurden aus dem Text abgeleitet."],
        image_signals=image_analysis.image_signals,
        confirmed_signals=image_analysis.confirmed_signals,
        assumptions=image_analysis.assumptions,
        missing_information=image_analysis.missing_information,
        confidence_notes=image_analysis.confidence_notes,
        conflicts=conflicts,
        image_analysis_failed=image_analysis_failed,
        image_analysis_warning=image_analysis_warning,
    )
    return updated


def log_image_analysis_failure(exc: Exception) -> None:
    logger.warning("SCENARIO_IMAGE_ANALYSIS_FALLBACK error=%r", exc)
