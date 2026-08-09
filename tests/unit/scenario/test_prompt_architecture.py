from pathlib import Path

from backend.core.llm.prompt_loader import PROMPT_PATHS, load_prompt


def test_all_registered_prompts_live_in_central_prompt_folder():
    for prompt_path in PROMPT_PATHS.values():
        assert prompt_path.parts[:2] == ("backend", "prompts")
        assert prompt_path.exists()


def test_vision_prompts_are_loaded_from_prompt_loader():
    scenario_prompt = load_prompt("scenario_image_analysis.prompt.txt")
    task_prompt = load_prompt("screenshot_task_structure.prompt.txt")

    assert "Szenariotext als separate Evidenz" in scenario_prompt
    assert "{scenario_text}" in scenario_prompt
    assert "user_goal" in task_prompt
    assert "hta_steps" in task_prompt


def test_screenshot_prompt_text_is_not_inline_in_multimodal_service():
    service_source = Path(
        "backend/domains/scenario/services/multimodal_analysis.py"
    ).read_text(encoding="utf-8")

    assert "Analysiere den Screenshot als Evidenzquelle" not in service_source
    assert "Analysiere den Screenshot als Vorbereitung" not in service_source
