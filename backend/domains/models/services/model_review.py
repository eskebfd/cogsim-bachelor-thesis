import json
import re

from backend.domains.models.schemas.revision_instruction import (
    RevisionInstructionSchema,
    TaskFeedbackClassification,
)
from backend.core.llm.client import llm
from backend.core.llm.prompt_loader import load_prompt
from backend.core.logging.workflow_logging import log_duration


structured_revision_instruction_model = llm.with_structured_output(
    RevisionInstructionSchema
)
structured_task_feedback_classification_model = llm.with_structured_output(
    TaskFeedbackClassification
)


def format_feedback(feedback: dict) -> str:
    if not feedback:
        return "Kein gezieltes Feedback angegeben."

    return json.dumps(
        feedback,
        ensure_ascii=False,
        indent=2,
    )


def _feedback_text(feedback: dict) -> str:
    if not feedback:
        return ""
    return " ".join(str(value) for value in feedback.values())


def _normalise_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _matching_steps(
    current_task_model: dict,
    feedback_text: str,
) -> tuple[list[str], list[str]]:
    normalized_feedback = _normalise_text(feedback_text)
    step_ids = []
    step_names = []

    for step in current_task_model.get("steps") or []:
        name = str(step.get("name") or "")
        normalized_name = _normalise_text(name)
        name_tokens = [
            token
            for token in re.findall(r"\w+", normalized_name)
            if len(token) > 3
        ]
        token_match = bool(name_tokens) and all(
            token in normalized_feedback for token in name_tokens
        )
        if name and (normalized_name in normalized_feedback or token_match):
            step_ids.append(str(step.get("step_id") or ""))
            step_names.append(name)

    return (
        [step_id for step_id in step_ids if step_id],
        step_names,
    )


def classify_task_feedback_heuristically(
    feedback: dict,
    current_task_model: dict,
) -> TaskFeedbackClassification:
    text = _normalise_text(_feedback_text(feedback))
    target_step_ids, target_step_names = _matching_steps(current_task_model, text)

    if not text:
        return TaskFeedbackClassification(
            change_type="ambiguous",
            target_step_ids=[],
            target_step_names=[],
            requested_change="Kein Feedback angegeben.",
            confidence=1.0,
            clarification_question="Welche Änderung soll an der HTA vorgenommen werden?",
        )

    if (
        target_step_names
        and any(keyword in text for keyword in ("dauert", "länger", "zeit", "seiten"))
    ):
        return TaskFeedbackClassification(
            change_type="update_timing",
            target_step_ids=target_step_ids,
            target_step_names=target_step_names,
            requested_change=_feedback_text(feedback),
            confidence=0.75,
            clarification_question=None,
        )

    if target_step_names and any(
        keyword in text
        for keyword in (
            "gedächtnis",
            "aufmerksamkeit",
            "kognitiv",
            "anforderung",
            "schwieriger",
        )
    ):
        return TaskFeedbackClassification(
            change_type="update_requirements",
            target_step_ids=target_step_ids,
            target_step_names=target_step_names,
            requested_change=_feedback_text(feedback),
            confidence=0.75,
            clarification_question=None,
        )

    if target_step_names and any(
        keyword in text for keyword in ("sollte", "anpassen", "präzisieren", "erweitern")
    ):
        return TaskFeedbackClassification(
            change_type="update_step",
            target_step_ids=target_step_ids,
            target_step_names=target_step_names,
            requested_change=_feedback_text(feedback),
            confidence=0.7,
            clarification_question=None,
        )

    if any(keyword in text for keyword in ("fehlt", "ergänz", "zusätzlich")) or (
        "noch" in text and not target_step_names
    ):
        return TaskFeedbackClassification(
            change_type="add_step",
            target_step_ids=target_step_ids,
            target_step_names=target_step_names,
            requested_change=_feedback_text(feedback),
            confidence=0.7,
            clarification_question=None,
        )

    patterns = (
        ("remove_step", ("nicht notwendig", "entfernen", "löschen", "falsch")),
        ("split_step", ("aufteilen", "trennen", "separat", "getrennt")),
        ("merge_steps", ("zusammenführen", "gemeinsam", "ein gemeinsamer")),
        ("reorder_steps", ("vor ", "nach ", "reihenfolge", "zuerst", "danach")),
        ("update_timing", ("dauert", "länger", "zeit", "seiten", "lesen")),
        (
            "update_requirements",
            (
                "gedächtnis",
                "aufmerksamkeit",
                "kognitiv",
                "anforderung",
                "schwieriger",
            ),
        ),
        ("add_step", ("muss", "noch", "ergänz", "fehlt", "zusätzlich")),
        ("update_step", ("sollte", "anpassen", "präzisieren", "erweitern")),
    )

    for change_type, keywords in patterns:
        if any(keyword in text for keyword in keywords):
            return TaskFeedbackClassification(
                change_type=change_type,
                target_step_ids=target_step_ids,
                target_step_names=target_step_names,
                requested_change=_feedback_text(feedback),
                confidence=0.65,
                clarification_question=None,
            )

    return TaskFeedbackClassification(
        change_type="ambiguous",
        target_step_ids=target_step_ids,
        target_step_names=target_step_names,
        requested_change=_feedback_text(feedback),
        confidence=0.45,
        clarification_question=(
            "Soll ein neuer Schritt ergänzt, ein vorhandener Schritt angepasst "
            "oder die Reihenfolge der HTA geändert werden?"
        ),
    )


def classify_task_feedback(
    scenario_description: str,
    feedback: dict,
    current_task_model: dict,
) -> TaskFeedbackClassification:
    heuristic = classify_task_feedback_heuristically(
        feedback,
        current_task_model,
    )
    if heuristic.change_type != "ambiguous" and heuristic.confidence >= 0.65:
        return heuristic

    prompt_template = load_prompt("task_feedback_classification.prompt.txt")
    prompt = prompt_template.format(
        scenario_description=scenario_description,
        current_task_model=json.dumps(
            current_task_model or {},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        feedback=format_feedback(feedback),
    )

    with log_duration(
        "llm.classify_task_feedback",
        prompt_chars=len(prompt),
    ):
        return structured_task_feedback_classification_model.invoke(prompt)


def generate_revision_instruction(
    scenario_description: str,
    feedback_target: str,
    feedback: dict,
    current_stage: str,
    current_task_model: dict | None = None,
) -> RevisionInstructionSchema:
    prompt_template = load_prompt("revision_instruction.prompt.txt")
    task_feedback_classification = None
    if feedback_target == "task_model":
        task_feedback_classification = classify_task_feedback(
            scenario_description,
            feedback,
            current_task_model or {},
        )

    prompt = prompt_template.format(
        scenario_description=scenario_description,
        current_stage=current_stage,
        feedback_target=feedback_target,
        feedback=format_feedback(feedback),
        task_feedback_classification=(
            task_feedback_classification.model_dump_json(indent=2)
            if task_feedback_classification
            else "Nicht zutreffend."
        ),
    )

    with log_duration(
        "llm.generate_revision_instruction",
        prompt_chars=len(prompt),
        feedback_target=feedback_target,
        current_stage=current_stage,
    ):
        revision_instruction = structured_revision_instruction_model.invoke(prompt)

    if task_feedback_classification is None:
        return revision_instruction

    if task_feedback_classification.change_type == "ambiguous":
        question = task_feedback_classification.clarification_question or (
            "Bitte präzisiere, welche HTA-Änderung vorgenommen werden soll."
        )
        return RevisionInstructionSchema(
            revision_instruction=(
                "AMBIGUOUS_TASK_FEEDBACK: Keine strukturelle Änderung am "
                f"Task Model vornehmen. Rückfrage: {question}"
            ),
            task_feedback_classification=task_feedback_classification,
        )

    return RevisionInstructionSchema(
        revision_instruction=(
            revision_instruction.revision_instruction
            + "\n\nKlassifizierte HTA-Änderung:\n"
            + task_feedback_classification.model_dump_json(indent=2)
        ),
        task_feedback_classification=task_feedback_classification,
    )
