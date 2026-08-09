from pathlib import Path

PROMPT_PATHS = {
    "scenario_dimension_context.prompt.txt": Path(
        "backend/prompts/scenario/dimension_context.prompt.txt"
    ),
    "scenario_task_dimensions.prompt.txt": Path(
        "backend/prompts/scenario/task_dimensions.prompt.txt"
    ),
    "scenario_interface_dimensions.prompt.txt": Path(
        "backend/prompts/scenario/interface_dimensions.prompt.txt"
    ),
    "scenario_environment_dimensions.prompt.txt": Path(
        "backend/prompts/scenario/environment_dimensions.prompt.txt"
    ),
    "task_model.prompt.txt": Path(
        "backend/prompts/models/task_model.prompt.txt"
    ),
    "interface_model.prompt.txt": Path(
        "backend/prompts/models/interface_model.prompt.txt"
    ),
    "environment_model.prompt.txt": Path(
        "backend/prompts/models/environment_model.prompt.txt"
    ),
    "revision_instruction.prompt.txt": Path(
        "backend/prompts/revisions/revision_instruction.prompt.txt"
    ),
    "task_feedback_classification.prompt.txt": Path(
        "backend/prompts/revisions/task_feedback_classification.prompt.txt"
    ),
    "scenario_image_analysis.prompt.txt": Path(
        "backend/prompts/vision/scenario_image_analysis.prompt.txt"
    ),
    "screenshot_task_structure.prompt.txt": Path(
        "backend/prompts/vision/screenshot_task_structure.prompt.txt"
    ),
    "simulation_plan_context.prompt.txt": Path(
        "backend/prompts/shared/simulation_plan_context.prompt.txt"
    ),
    "current_task_model_revision_context.prompt.txt": Path(
        "backend/prompts/revisions/current_task_model_revision_context.prompt.txt"
    ),
}


def load_prompt(filename: str) -> str:

    prompt_path = PROMPT_PATHS[filename]

    with open(
        prompt_path,
        "r",
        encoding="utf-8",
    ) as file:

        return file.read()
