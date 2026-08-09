from __future__ import annotations

import re
from copy import deepcopy
from typing import Any


TASK_ATTRIBUTE_IDS = (
    "task_complexity",
    "number_of_steps",
    "reading_demand",
    "unfamiliar_word_density",
    "orthographic_irregularity",
    "morphological_complexity",
    "input_demand",
    "memory_demand",
    "decision_demand",
    "error_criticality",
)


def _clamp_score(value: float) -> int:
    return max(0, min(100, round(value)))


def _normalise_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _step_signature(step: dict) -> str:
    name = _normalise_text(step.get("name"))
    description = _normalise_text(step.get("description"))
    goal = _normalise_text(step.get("goal"))
    return " | ".join(part for part in (name, description, goal) if part)


def _step_matches(left: dict, right: dict) -> bool:
    left_signature = _step_signature(left)
    right_signature = _step_signature(right)
    if left_signature and right_signature and left_signature == right_signature:
        return True

    left_name = _normalise_text(left.get("name"))
    right_name = _normalise_text(right.get("name"))
    return bool(left_name and right_name and left_name == right_name)


def _find_matching_step_index(
    steps: list[dict],
    candidate: dict,
    used_indices: set[int] | None = None,
) -> int | None:
    used_indices = used_indices or set()
    for index, step in enumerate(steps):
        if index in used_indices:
            continue
        if _step_matches(step, candidate):
            return index
    return None


def _renumber_steps(steps: list[dict]) -> list[dict]:
    renumbered = []
    for index, step in enumerate(steps, start=1):
        updated = deepcopy(step)
        updated["step_id"] = f"step_{index}"
        renumbered.append(updated)
    return renumbered


def _merge_step_update(current_step: dict, revised_step: dict) -> dict:
    merged = {
        **deepcopy(current_step),
        **deepcopy(revised_step),
    }
    for key in (
        "goms_operations",
        "operation_time_estimates",
        "cognitive_requirements",
    ):
        if not revised_step.get(key) and current_step.get(key):
            merged[key] = deepcopy(current_step[key])
    if not revised_step.get("estimated_duration_seconds"):
        merged["estimated_duration_seconds"] = current_step.get(
            "estimated_duration_seconds"
        )
    return merged


def merge_task_model_revision(
    current_task_model: dict,
    revised_task_model: dict,
) -> dict:
    current_model = deepcopy(current_task_model or {})
    revised_model = deepcopy(revised_task_model or {})
    current_steps = list(current_model.get("steps") or [])
    revised_steps = list(revised_model.get("steps") or [])

    if not current_steps:
        return normalize_task_model_attributes(revised_model)
    if not revised_steps:
        return normalize_task_model_attributes(current_model)

    merged_steps: list[dict] = []
    used_current_indices: set[int] = set()

    for revised_step in revised_steps:
        current_index = _find_matching_step_index(
            current_steps,
            revised_step,
            used_current_indices,
        )
        if current_index is None:
            if _find_matching_step_index(merged_steps, revised_step) is None:
                merged_steps.append(deepcopy(revised_step))
            continue

        merged_steps.append(
            _merge_step_update(
                current_steps[current_index],
                revised_step,
            )
        )
        used_current_indices.add(current_index)

    for index, current_step in enumerate(current_steps):
        if index not in used_current_indices:
            merged_steps.append(deepcopy(current_step))

    merged_model = {
        **current_model,
        **revised_model,
        "steps": _renumber_steps(merged_steps),
    }
    return normalize_task_model_attributes(
        merged_model,
        baseline_task_model=current_model,
        preserve_existing_minimum=len(merged_steps) > len(current_steps),
    )


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def _step_text(step: dict) -> str:
    values = [
        step.get("name"),
        step.get("goal"),
        step.get("step_type"),
        step.get("description"),
        " ".join(step.get("goms_operations") or []),
        " ".join(step.get("cognitive_requirements") or []),
    ]
    return _normalise_text(" ".join(str(value or "") for value in values))


def _step_duration(step: dict) -> float:
    try:
        return float(step.get("estimated_duration_seconds") or 0)
    except (TypeError, ValueError):
        return 0


def _ratio_score(
    matching_steps: int,
    step_count: int,
    *,
    ratio_weight: float,
    count_weight: float = 0,
    maximum_count_bonus: int = 6,
) -> float:
    if step_count <= 0 or matching_steps <= 0:
        return 0

    ratio = matching_steps / step_count
    count_bonus = min(matching_steps, maximum_count_bonus) * count_weight
    return ratio * ratio_weight + count_bonus


def _average_matching_duration(
    steps: list[dict],
    step_texts: list[str],
    keywords: tuple[str, ...],
) -> float:
    matching_durations = [
        _step_duration(step)
        for step, text in zip(steps, step_texts)
        if _contains_any(text, keywords)
    ]
    if not matching_durations:
        return 0
    return sum(matching_durations) / len(matching_durations)


def _duration_component(
    duration_seconds: float,
    *,
    max_duration_seconds: float,
    weight: float,
) -> float:
    if duration_seconds <= 0:
        return 0
    return min(duration_seconds, max_duration_seconds) / max_duration_seconds * weight


def _attribute_value(
    model: dict,
    attribute_id: str,
) -> int | None:
    attribute = model.get(attribute_id)
    if isinstance(attribute, dict):
        attribute = attribute.get("value")

    try:
        return _clamp_score(float(attribute))
    except (TypeError, ValueError):
        return None


def _attribute_with_updated_value(
    task_model: dict,
    attribute_id: str,
    value: int,
    explanation: str,
) -> dict:
    current = deepcopy(task_model.get(attribute_id) or {})
    current["value"] = _clamp_score(value)
    current.setdefault("scale_min_description", "gering ausgeprägt")
    current.setdefault("scale_max_description", "stark ausgeprägt")
    current["explanation"] = explanation
    current["confidence"] = current.get("confidence") or "medium"
    return current


def derive_task_attribute_values(task_model: dict) -> dict[str, int]:
    steps = list(task_model.get("steps") or [])
    step_count = len(steps)
    step_texts = [_step_text(step) for step in steps]
    durations = [_step_duration(step) for step in steps]
    total_duration = sum(durations)
    average_duration = total_duration / step_count if step_count else 0
    reading_keywords = ("read", "lesen", "text", "information", "prüfen")
    input_keywords = (
        "input",
        "type",
        "eingabe",
        "ausfüllen",
        "formular",
        "select",
        "click",
    )
    memory_keywords = ("merken", "erinner", "vergleich", "zurück", "daten")
    decision_keywords = (
        "decide",
        "entscheid",
        "auswahl",
        "wählen",
        "vergleichen",
        "filter",
    )
    error_keywords = (
        "submit",
        "absenden",
        "buch",
        "zahlung",
        "fehler",
        "kritisch",
        "pflicht",
    )

    reading_steps = sum(
        1
        for text in step_texts
        if _contains_any(text, reading_keywords)
    )
    input_steps = sum(
        1
        for text in step_texts
        if _contains_any(text, input_keywords)
    )
    memory_steps = sum(
        1
        for text in step_texts
        if _contains_any(text, memory_keywords)
    )
    decision_steps = sum(
        1
        for text in step_texts
        if _contains_any(text, decision_keywords)
    )
    error_steps = sum(
        1
        for text in step_texts
        if _contains_any(text, error_keywords)
    )
    unfamiliar_word_steps = sum(
        1
        for text in step_texts
        if _contains_any(
            text,
            (
                "unbekannt",
                "fachbegriff",
                "fachlich",
                "produktname",
                "hotelname",
                "fremdwort",
                "terminologie",
            ),
        )
    )
    orthographic_steps = sum(
        1
        for text in step_texts
        if _contains_any(
            text,
            (
                "orthograf",
                "irregulär",
                "fremdsprach",
                "schreibweise",
                "eigenname",
                "produktname",
                "hotelname",
            ),
        )
    )
    morphology_steps = sum(
        1
        for text in step_texts
        if _contains_any(
            text,
            (
                "lang",
                "zusammengesetzt",
                "mehrteilig",
                "komplexe wörter",
                "wortform",
                "ableitung",
            ),
        )
    )

    reading_duration = _average_matching_duration(
        steps,
        step_texts,
        reading_keywords,
    )
    step_scope_score = _clamp_score(min(step_count, 10) * 6 + max(step_count - 4, 0) * 2)
    duration_score = _clamp_score(
        _duration_component(
            average_duration,
            max_duration_seconds=75,
            weight=55,
        )
        + _duration_component(
            total_duration,
            max_duration_seconds=420,
            weight=25,
        )
    )
    reading_demand = _clamp_score(
        _ratio_score(
            reading_steps,
            step_count,
            ratio_weight=58,
            count_weight=3,
        )
        + _duration_component(
            reading_duration,
            max_duration_seconds=120,
            weight=28,
        )
    )
    unfamiliar_word_density = _clamp_score(
        _ratio_score(
            unfamiliar_word_steps,
            step_count,
            ratio_weight=64,
            count_weight=3,
        )
        + _ratio_score(
            reading_steps,
            step_count,
            ratio_weight=10,
        )
    )
    orthographic_irregularity = _clamp_score(
        _ratio_score(
            orthographic_steps,
            step_count,
            ratio_weight=66,
            count_weight=3,
        )
        + _ratio_score(
            unfamiliar_word_steps,
            step_count,
            ratio_weight=12,
        )
    )
    morphological_complexity = _clamp_score(
        _ratio_score(
            morphology_steps,
            step_count,
            ratio_weight=64,
            count_weight=3,
        )
        + _ratio_score(
            reading_steps,
            step_count,
            ratio_weight=8,
        )
    )
    input_demand = _clamp_score(
        _ratio_score(
            input_steps,
            step_count,
            ratio_weight=68,
            count_weight=4,
        )
    )
    memory_demand = _clamp_score(
        _ratio_score(
            memory_steps,
            step_count,
            ratio_weight=62,
            count_weight=4,
        )
        + min(max(step_count - 3, 0), 7) * 4
    )
    decision_demand = _clamp_score(
        _ratio_score(
            decision_steps,
            step_count,
            ratio_weight=70,
            count_weight=4,
        )
    )
    error_criticality = _clamp_score(
        _ratio_score(
            error_steps,
            step_count,
            ratio_weight=72,
            count_weight=4,
        )
        + _ratio_score(
            decision_steps,
            step_count,
            ratio_weight=10,
        )
    )
    demand_values = [
        reading_demand,
        unfamiliar_word_density,
        orthographic_irregularity,
        morphological_complexity,
        input_demand,
        memory_demand,
        decision_demand,
        error_criticality,
    ]
    average_demand = sum(demand_values) / len(demand_values)
    task_complexity = _clamp_score(
        (15 if step_count else 0)
        + step_scope_score * 0.35
        + duration_score * 0.2
        + max(demand_values) * 0.2
        + average_demand * 0.2
    )

    return {
        "task_complexity": task_complexity,
        "number_of_steps": step_count,
        "reading_demand": reading_demand,
        "unfamiliar_word_density": unfamiliar_word_density,
        "orthographic_irregularity": orthographic_irregularity,
        "morphological_complexity": morphological_complexity,
        "input_demand": input_demand,
        "memory_demand": memory_demand,
        "decision_demand": decision_demand,
        "error_criticality": error_criticality,
    }


def normalize_task_model_attributes(
    task_model: dict,
    *,
    baseline_task_model: dict | None = None,
    preserve_existing_minimum: bool = False,
) -> dict:
    updated = deepcopy(task_model)
    values = derive_task_attribute_values(updated)
    if preserve_existing_minimum and baseline_task_model:
        for attribute_id in TASK_ATTRIBUTE_IDS:
            if attribute_id == "number_of_steps":
                continue
            baseline_value = _attribute_value(
                baseline_task_model,
                attribute_id,
            )
            if baseline_value is not None:
                values[attribute_id] = max(
                    values[attribute_id],
                    baseline_value,
                )

    explanations = {
        "task_complexity": (
            "Deterministisch aus Anzahl, Dauer, Interaktions-, Lese-, "
            "Gedächtnis-, Entscheidungs- und Fehlerrisikoanteilen der aktuellen HTA abgeleitet."
        ),
        "number_of_steps": (
            f"Reale Anzahl der aktuellen HTA-Hauptschritte: {values['number_of_steps']}."
        ),
        "reading_demand": (
            "Deterministisch aus lesenden, prüfenden und informationsbezogenen HTA-Schritten abgeleitet."
        ),
        "unfamiliar_word_density": (
            "Deterministisch aus Hinweisen auf unbekannte, seltene oder fachliche Wörter in der aktuellen HTA abgeleitet."
        ),
        "orthographic_irregularity": (
            "Deterministisch aus Hinweisen auf fremdsprachige, eigenständige oder schwer ableitbare Schreibweisen abgeleitet."
        ),
        "morphological_complexity": (
            "Deterministisch aus Hinweisen auf lange, mehrteilige oder komplexe Wortformen abgeleitet."
        ),
        "input_demand": (
            "Deterministisch aus Eingabe-, Auswahl-, Klick- und Formularschritten abgeleitet."
        ),
        "memory_demand": (
            "Deterministisch aus Merken-, Vergleichs- und mehrschrittigen HTA-Anforderungen abgeleitet."
        ),
        "decision_demand": (
            "Deterministisch aus Entscheidungs-, Auswahl-, Vergleichs- und Filterschritten abgeleitet."
        ),
        "error_criticality": (
            "Deterministisch aus kritischen Absende-, Pflicht-, Buchungs- oder Fehlerstellen abgeleitet."
        ),
    }
    for attribute_id in TASK_ATTRIBUTE_IDS:
        updated[attribute_id] = _attribute_with_updated_value(
            updated,
            attribute_id,
            values[attribute_id],
            explanations[attribute_id],
        )
    return updated
