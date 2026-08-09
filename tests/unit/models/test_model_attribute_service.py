from types import SimpleNamespace

import httpx
import pytest
from openai import APITimeoutError

from backend.domains.models.schemas.environment import EnvironmentModelSchema
from backend.domains.scenario.schemas.dimensions import ScenarioDimensionsSchema
from backend.domains.models.schemas.task import TaskModelSchema
from backend.domains.planning.services.computed_parameters import (
    build_computed_task_parameters,
)
from backend.domains.models.services.model_attributes import (
    ModelAttributeError,
    numeric_attribute_value,
)
from backend.core.llm.client import (
    WorkflowLLMTimeoutError,
    build_simulation_plan_prompt_context,
    invoke_structured,
)
from backend.domains.evaluation.registries.metrics import get_metric_by_id
from backend.domains.planning.services.simulation_plan import (
    build_simulation_plan_for_profile_ids,
)
import backend.core.llm.client as llm_service
from tests.fixtures.frontend_mock_data import (
    MOCK_DIMENSIONS,
    MOCK_ENVIRONMENT_MODEL,
    MOCK_INTERFACE_MODEL,
    MOCK_TASK_MODEL,
)


def test_numeric_attribute_value_supports_number_dict_and_object():
    assert numeric_attribute_value({"noise_level": 35}, "noise_level") == 35
    assert numeric_attribute_value(
        {"noise_level": {"value": 70}}, "noise_level"
    ) == 70
    assert numeric_attribute_value(
        {"noise_level": SimpleNamespace(value=45)}, "noise_level"
    ) == 45


def test_numeric_attribute_value_uses_default_or_clear_error():
    assert numeric_attribute_value({}, "noise_level", default=50) == 50

    with pytest.raises(ModelAttributeError, match="noise_level"):
        numeric_attribute_value({}, "noise_level")


def test_computed_parameters_accept_structured_attribute_objects():
    result = build_computed_task_parameters(
        MOCK_TASK_MODEL,
        MOCK_INTERFACE_MODEL,
    ).model_dump()

    assert result["text_complexity"]["value"] == 30
    assert result["navigation_effort"]["value"] == 29
    assert "decoding_load" in result
    assert "visual_reading_load" in result
    assert "dyslexia_reading_load" in result
    assert "sustained_attention_load" in result
    assert "inhibition_load" in result
    assert "attention_switching_load" in result
    assert "adhd_interaction_load" in result


def test_dyslexia_computed_parameters_use_task_and_interface_factors():
    task_model = {
        **MOCK_TASK_MODEL,
        "reading_demand": {"value": 70},
        "unfamiliar_word_density": {"value": 80},
        "orthographic_irregularity": {"value": 75},
        "morphological_complexity": {"value": 65},
    }
    interface_model = {
        **MOCK_INTERFACE_MODEL,
        "text_density": {"value": 70},
        "line_tracking_difficulty": {"value": 60},
        "visual_clutter": {"value": 50},
        "text_legibility": {"value": 40},
    }

    result = build_computed_task_parameters(
        task_model,
        interface_model,
    ).model_dump()

    assert result["decoding_load"]["value"] == 72
    assert result["visual_reading_load"]["value"] == 60
    assert result["dyslexia_reading_load"]["value"] == 58


def test_adhd_computed_parameters_use_attention_and_interface_factors():
    task_model = {
        **MOCK_TASK_MODEL,
        "sustained_attention_demand": {"value": 70},
        "task_switching_demand": {"value": 80},
        "inhibition_demand": {"value": 65},
        "divided_attention_demand": {"value": 75},
        "task_complexity": {"value": 60},
        "memory_demand": {"value": 50},
    }
    interface_model = {
        **MOCK_INTERFACE_MODEL,
        "irrelevant_signal_load": {"value": 70},
        "feedback_interruptiveness": {"value": 60},
        "visual_clutter": {"value": 55},
        "navigation_complexity": {"value": 60},
    }

    result = build_computed_task_parameters(
        task_model,
        interface_model,
    ).model_dump()

    assert result["inhibition_load"]["value"] >= 62
    assert result["attention_switching_load"]["value"] >= 65
    assert result["adhd_interaction_load"]["value"] >= 50


def test_enriched_model_schemas_accept_current_fixtures():
    dimensions = ScenarioDimensionsSchema.model_validate(MOCK_DIMENSIONS)
    task_model = TaskModelSchema.model_validate(MOCK_TASK_MODEL)
    environment_model = EnvironmentModelSchema.model_validate(
        MOCK_ENVIRONMENT_MODEL
    )

    assert dimensions.task_signals.memory_demand.value == 45
    assert dimensions.task_signals.unfamiliar_word_density.value == 20
    assert dimensions.task_signals.orthographic_irregularity.value == 15
    assert dimensions.task_signals.morphological_complexity.value == 25
    assert dimensions.task_signals.sustained_attention_demand.value == 40
    assert dimensions.task_signals.task_switching_demand.value == 45
    assert dimensions.task_signals.inhibition_demand.value == 30
    assert dimensions.task_signals.divided_attention_demand.value == 45
    assert dimensions.interface_signals.text_legibility.value == 70
    assert dimensions.interface_signals.text_density.value == 35
    assert dimensions.interface_signals.line_tracking_difficulty.value == 25
    assert dimensions.interface_signals.stimulus_density.value == 45
    assert dimensions.interface_signals.irrelevant_signal_load.value == 25
    assert dimensions.interface_signals.feedback_interruptiveness.value == 30
    assert dimensions.interface_signals.focus_guidance.value == 60
    assert dimensions.environment_signals.distractions.value == 55
    assert dimensions.environment_signals.external_interruption_frequency.value == 45
    assert dimensions.environment_signals.attention_recovery_support.value == 60
    assert "user_signals" not in dimensions.model_dump()
    assert "suggested_task_parameters" not in dimensions.model_dump()
    assert task_model.error_criticality.value == 60
    assert environment_model.interruption_risk.value == 55


def test_structured_llm_parsing_error_logs_raw_response(caplog):
    class InvalidStructuredModel:
        def invoke(self, prompt):
            return {
                "parsed": None,
                "parsing_error": ValueError("invalid structured output"),
                "raw": SimpleNamespace(content="not valid model data"),
            }

    with pytest.raises(ValueError, match="invalid structured output"):
        invoke_structured(
            InvalidStructuredModel(),
            "prompt",
            "structured_output_test",
        )

    assert "not valid model data" in caplog.text


def test_scenario_dimensions_timeout_is_retried_once(caplog):
    class TimeoutModel:
        calls = 0

        def invoke(self, prompt):
            self.calls += 1
            raise APITimeoutError(
                request=httpx.Request("POST", "https://example.test")
            )

    model = TimeoutModel()

    with pytest.raises(WorkflowLLMTimeoutError) as exc_info:
        invoke_structured(
            model,
            "prompt",
            "scenario_dimensions",
            timeout_retries=1,
        )

    assert model.calls == 2
    assert exc_info.value.workflow_step == "scenario_dimensions"
    assert caplog.text.count("LLM_TIMEOUT") == 2


def test_interface_model_enables_one_timeout_retry(monkeypatch):
    captured = {}

    def fake_invoke(model, prompt, stage, timeout_retries=0):
        captured.update(
            {
                "stage": stage,
                "timeout_retries": timeout_retries,
                "prompt": prompt,
            }
        )
        return "interface-model"

    monkeypatch.setattr(llm_service, "invoke_structured", fake_invoke)

    result = llm_service.generate_interface_model(
        scenario_context={
            "description": "Kursanmeldung",
            "task": {"label": "Kurs auswählen"},
            "task_parameters": {},
        },
        scenario_dimensions={
            "interface_signals": {
                "visual_clutter": {"value": 50},
            }
        },
    )

    assert result == "interface-model"
    assert captured["stage"] == "interface_model"
    assert captured["timeout_retries"] == 1
    assert len(captured["prompt"]) < 5000
    assert "SIMULATION PLAN CONTEXT" not in captured["prompt"]


def test_simulation_plan_context_is_empty_when_plan_is_missing():
    assert build_simulation_plan_prompt_context(None) == ""


def test_interface_model_accepts_compact_simulation_plan_context(monkeypatch):
    captured = {}
    metric = get_metric_by_id("cognitive_load")
    assert metric is not None
    plan = build_simulation_plan_for_profile_ids(["adhd"], [metric])

    def fake_invoke(model, prompt, stage, timeout_retries=0):
        captured["prompt"] = prompt
        return "interface-model"

    monkeypatch.setattr(llm_service, "invoke_structured", fake_invoke)

    result = llm_service.generate_interface_model(
        scenario_context={
            "description": "Kursanmeldung",
            "task": {"label": "Kurs auswählen"},
            "task_parameters": {},
        },
        scenario_dimensions={},
        simulation_plan=plan,
    )

    assert result == "interface-model"
    assert "SIMULATION PLAN CONTEXT" in captured["prompt"]
    assert '"cognitive_load"' in captured["prompt"]
    assert '"generic"' in captured["prompt"]
    assert '"adhd"' in captured["prompt"]
    assert metric.description not in captured["prompt"]


def test_plan_computation_model_controls_computed_task_parameter():
    metric = get_metric_by_id("cognitive_load")
    assert metric is not None
    plan = build_simulation_plan_for_profile_ids(["generic"], [metric])
    text_model = next(
        model
        for model in plan.computation_models
        if model.output == "text_complexity"
    )
    text_model.weights = {
        "text_volume": 1.0,
        "sentence_length": 0.0,
        "word_difficulty": 0.0,
        "technical_terms": 0.0,
    }

    result = build_computed_task_parameters(
        MOCK_TASK_MODEL,
        MOCK_INTERFACE_MODEL,
        simulation_plan=plan,
    )

    assert result.text_complexity.value == MOCK_INTERFACE_MODEL["text_volume"][
        "value"
    ]
