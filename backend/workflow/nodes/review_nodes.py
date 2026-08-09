from backend.workflow.state import CogSimState
from backend.domains.models.services.model_review import generate_revision_instruction
from backend.core.logging.workflow_logging import log_duration


def prepare_revision_instruction_node(
    state: CogSimState,
) -> CogSimState:
    with log_duration(
        "node.prepare_revision_instruction",
        current_stage=state.get("current_stage", ""),
        feedback_target=state.get("feedback_target", ""),
    ):
        revision_result = generate_revision_instruction(
            scenario_description=state.get("scenario_description", ""),
            feedback_target=state.get("feedback_target", ""),
            feedback=state.get("feedback", {}),
            current_stage=state.get("current_stage", ""),
            current_task_model=state.get("task_model", {}),
        )
        revision_data = revision_result.model_dump()
        classification = revision_data.get("task_feedback_classification")
        if (
            state.get("feedback_target") == "task_model"
            and classification
            and classification.get("change_type") == "ambiguous"
        ):
            return {
                **state,
                "current_stage": "finished",
                "revision_instruction": revision_data.get(
                    "revision_instruction",
                    "",
                ),
                "last_feedback": {
                    "current_stage": state.get("current_stage", ""),
                    "feedback_target": state.get("feedback_target", ""),
                    "feedback": state.get("feedback", {}),
                    "task_feedback_classification": classification,
                },
            }

        return {
            **state,
            "revision_instruction": revision_data.get(
                "revision_instruction",
                "",
            ),
            "last_feedback": {
                "current_stage": state.get("current_stage", ""),
                "feedback_target": state.get("feedback_target", ""),
                "feedback": state.get("feedback", {}),
                "task_feedback_classification": classification,
            },
        }
