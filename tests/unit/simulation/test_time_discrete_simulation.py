import pytest

from backend.domains.simulation.algorithms.computed_parameters import (
    calculate_navigation_effort,
    calculate_text_complexity,
)
from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.engine import (
    calculate_task_progress_rate,
    normalized_task_steps,
    run_time_discrete_simulation,
    simulate,
    simulate_many,
)
from backend.workflow.nodes.simulation_nodes import run_simulation_step
from backend.domains.simulation.schemas.simulation_model import SimulationModelSchema
from backend.domains.models.schemas.task import TaskStepSchema
from backend.domains.simulation.metrics import calculate_result_metrics
from backend.domains.simulation.results import derive_profile_insights
from backend.domains.simulation.algorithms.state_updates import (
    calculate_attention_decay,
    calculate_fatigue_target,
    calculate_reading_speed,
    update_attention,
)
from backend.domains.simulation.values import validated_weights
from backend.domains.simulation.weights import normalize_weights
from frontend.features.simulation.results import (
    build_profile_result_views,
    build_simulation_csv,
    build_simulation_table_rows,
    build_timeline_rows,
    build_simulation_export,
)
from frontend.features.computed_parameters.view import build_computed_parameter_rows


def attribute(value: int) -> dict:
    return {"value": value}


def simulation_inputs(duration_seconds: int = 3) -> tuple[dict, ...]:
    return (
        {
            "reading_difficulty": attribute(60),
            "attention_stability": attribute(70),
            "distraction_sensitivity": attribute(40),
        },
        {
            "task_complexity": attribute(60),
            "number_of_steps": attribute(20),
            "reading_demand": attribute(50),
            "input_demand": attribute(40),
            "memory_demand": attribute(30),
            "steps": [
                {
                    "step_id": "step_1",
                    "name": "Hinweise lesen",
                    "goal": "Hinweise verstehen",
                    "step_type": "read",
                    "description": "Den Einführungstext lesen.",
                    "goms_operations": ["read", "think"],
                    "estimated_duration_seconds": duration_seconds,
                }
            ],
        },
        {
            "text_volume": attribute(50),
            "sentence_length": attribute(50),
            "word_difficulty": attribute(50),
            "technical_terms": attribute(50),
            "visual_clutter": attribute(40),
            "navigation_complexity": attribute(30),
            "accessibility_support": attribute(20),
        },
        {
            "noise_level": attribute(30),
            "distractions": attribute(40),
            "time_pressure": attribute(50),
            "context_stability": attribute(60),
        },
        {
            "text_complexity": {"value": 50},
            "navigation_effort": {"value": 30},
        },
    )


def simulation_model() -> dict:
    return {
        "time_step_seconds": 2,
        "initial_user_state": {"attention": 55, "fatigue": 20},
        "response_rates": {"attention": 0, "fatigue": 0.1},
        "event_thresholds": {
            "high_error_risk": 70,
            "very_high_cognitive_load": 80,
            "very_low_attention": 15,
            "high_dyslexia_reading_load": 65,
        },
        "model_weights": {
            "text_complexity": [0.25, 0.25, 0.25, 0.25],
            "navigation_effort": [1 / 3, 1 / 3, 1 / 3],
            "decoding_load": [0.25, 0.25, 0.25, 0.25],
            "visual_reading_load": [0.25, 0.25, 0.25, 0.25],
            "dyslexia_reading_load": [0.35, 0.25, 0.25, 0.15],
            "reading_speed": [0.25, 0.25, 0.25, 0.25],
            "attention": [1 / 6] * 6,
            "fatigue": [0.2] * 5,
            "cognitive_load": [0.2] * 5,
            "error_risk": [0.25] * 4,
            "task_success_score": [1 / 3] * 3,
            "completion_efficiency": [1 / 3] * 3,
        },
        "task_step_modifiers": [
            {
                "step_id": "step_1",
                "attention_modifier": 1,
                "fatigue_modifier": 1,
                "reading_speed_modifier": 0.5,
                "reason": "Leseschritt mit reduzierter Verarbeitungsgeschwindigkeit.",
            }
        ],
        "assumptions": ["Zwei Sekunden pro Simulationsintervall."],
    }


def test_backend_golden_path_reports_comparable_result_metrics():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=4)
    )
    result = run_time_discrete_simulation(
        user_model,
        task_model,
        interface_model,
        environment_model,
        {
            **parameters,
            "dyslexia_reading_load": {"value": 42},
            "adhd_interaction_load": {"value": 37},
        },
        config=SimulationConfig(
            enable_task_abandonment=False,
            max_duration_seconds=30,
        ),
    )

    assert result["completed"] is True
    assert result["timeline"]
    assert result["timeline"][-1]["task_progress"] == pytest.approx(1.0)
    assert result["completion_time_seconds"] > 0
    assert result["task_step_durations"][0]["actual_step_duration"] > 0
    for metric_id in (
        "cognitive_load",
        "error_risk",
        "task_success_score",
        "completion_efficiency",
        "completion_time",
        "time_limit_risk",
    ):
        assert metric_id in result["final_metrics"]
    assert result["final_metrics"]["completion_time"] == (
        result["completion_time_seconds"]
    )
    assert "dyslexia_reading_load" not in result["final_metrics"]
    assert "adhd_interaction_load" not in result["final_metrics"]


def test_normalize_weights_corrects_invalid_sums_and_zero_values():
    assert normalize_weights([0.25, 0.25, 0.25]) == [
        0.3333,
        0.3333,
        0.3334,
    ]
    assert normalize_weights([0.2, 0.3, 0.4]) == [
        0.2222,
        0.3333,
        0.4445,
    ]
    assert normalize_weights([0, 0, 0]) == [0.3333, 0.3333, 0.3334]
    assert normalize_weights([]) == [0.3333, 0.3333, 0.3334]


def test_simulation_model_schema_normalizes_llm_style_weight_errors(caplog):
    payload = simulation_model()
    payload["model_weights"]["fatigue"] = [0.2, 0.3, 0.4, 0.05, 0.01]

    model = SimulationModelSchema.model_validate(payload)

    assert sum(model.model_weights.fatigue) == pytest.approx(1.0)
    assert model.model_weights.fatigue == normalize_weights(
        [0.2, 0.3, 0.4, 0.05, 0.01]
    )
    assert "NORMALIZE_SIMULATION_WEIGHTS" in caplog.text
    assert "fatigue" in caplog.text


def test_simulation_model_schema_accepts_legacy_task_success_weight_key():
    payload = simulation_model()
    payload["model_weights"].pop("task_success_score")
    payload["model_weights"]["task_success_probability"] = [0.2, 0.3, 0.5]

    model = SimulationModelSchema.model_validate(payload)

    assert model.model_weights.task_success_score == [0.2, 0.3, 0.5]


def test_task_step_schema_requires_goms_duration():
    step = TaskStepSchema(
        step_id="step_1",
        name="Hinweise lesen",
        goal="Hinweise verstehen",
        description="Einführung lesen",
        step_type="read",
        goms_operations=["read", "think"],
        estimated_duration_seconds=5,
    )

    assert step.estimated_duration_seconds == 5

    with pytest.raises(ValueError):
        TaskStepSchema(
            step_id="step_1",
            name="Hinweise lesen",
            goal="Hinweise verstehen",
            description="Einführung lesen",
            step_type="read",
            goms_operations=["read"],
            estimated_duration_seconds=0,
        )


def test_missing_task_duration_falls_back_to_one_second(caplog):
    steps = normalized_task_steps(
        {"steps": [{"step_id": "step_1", "name": "Start"}]}
    )

    assert steps[0]["duration_seconds"] == 1
    assert "SIMULATION_DURATION_FALLBACK" in caplog.text


def test_task_progress_rate_decreases_with_profile_load():
    task_step = {"step_type": "read"}
    strong_rate = calculate_task_progress_rate(
        task_step,
        {"reading_speed": 80, "attention": 90, "fatigue": 10},
        {"cognitive_load": 20, "error_risk": 10},
        navigation_effort=20,
    )
    impaired_rate = calculate_task_progress_rate(
        task_step,
        {"reading_speed": 45, "attention": 35, "fatigue": 75},
        {"cognitive_load": 80, "error_risk": 70},
        navigation_effort=20,
    )

    assert impaired_rate < strong_rate


def test_simulation_model_schema_and_config_override_defaults():
    configured_model = SimulationModelSchema.model_validate(simulation_model())
    inputs = simulation_inputs(duration_seconds=3)

    result = run_time_discrete_simulation(
        *inputs,
        simulation_model=configured_model.model_dump(),
    )

    assert result["simulation_model_used"] is True
    assert result["time_step_seconds"] == 2
    assert result["total_duration_seconds"] > 3
    assert result["timeline"][-1]["task_progress"] == 1
    assert result["initial_user_state"] == {
        "reading_speed": 0.0,
        "attention": 55.0,
        "fatigue": 20.0,
    }
    assert result["timeline"][0]["attention"] == 55.0
    assert 0 < result["timeline"][0]["reading_speed"] < 35.0


def test_simulation_without_simulation_model_uses_config_defaults():
    inputs = simulation_inputs(duration_seconds=2)

    implicit = run_time_discrete_simulation(*inputs)
    explicit = run_time_discrete_simulation(*inputs, simulation_model={})

    assert implicit["simulation_model_used"] is False
    assert implicit["time_step_seconds"] == 1
    assert implicit["timeline"] == explicit["timeline"]
    assert len(implicit["timeline"]) > 2


def test_simulate_preserves_legacy_single_run_behavior():
    inputs = simulation_inputs(duration_seconds=2)

    legacy_result = run_time_discrete_simulation(*inputs)
    result = simulate(*inputs)

    assert result == legacy_result


def test_simulate_many_keeps_results_assigned_to_profiles():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=2)
    )
    adhd_model = {
        **user_model,
        "attention_stability": attribute(35),
        "distraction_sensitivity": attribute(75),
    }

    result = simulate_many(
        user_models={"generic": user_model, "adhd": adhd_model},
        task_model=task_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=parameters,
        profile_labels={"generic": "Generic", "adhd": "ADHD"},
        baseline_profile_id="generic",
    )

    assert result["profile_ids"] == ["generic", "adhd"]
    assert result["profile_count"] == 2
    assert result["baseline_profile_id"] == "generic"
    assert list(result["results_by_profile"]) == ["generic", "adhd"]
    assert [run["profile_id"] for run in result["runs"]] == [
        "generic",
        "adhd",
    ]
    assert result["runs"][1]["user_model"] == adhd_model
    assert result["results_by_profile"]["adhd"]["profile_label"] == "ADHD"
    assert result["results_by_profile"]["adhd"]["final_state"] == result[
        "results_by_profile"
    ]["adhd"]["final_user_state"]
    assert result["runs"][0]["metrics"] == result["runs"][0][
        "final_metrics"
    ]
    assert result["runs"][0]["timeline"]
    assert "events" in result["runs"][0]
    assert set(result["comparison_summary"]) == {
        "problems",
        "recommendations",
    }


def test_three_user_models_create_three_profile_timelines():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=1)
    )
    user_models = {
        "generic": user_model,
        "adhd": {
            **user_model,
            "attention_stability": attribute(35),
        },
        "dyslexie": {
            **user_model,
            "reading_difficulty": attribute(75),
        },
    }

    result = simulate_many(
        user_models=user_models,
        task_model=task_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=parameters,
        profile_labels={"generic": "Generic", "adhd": "ADHS", "dyslexie": "Dyslexie"},
        baseline_profile_id="generic",
    )

    assert result["profile_ids"] == ["generic", "adhd", "dyslexie"]
    assert all(
        result["results_by_profile"][profile_id]["timeline"]
        for profile_id in result["profile_ids"]
    )


def test_simulation_node_keeps_baseline_result_and_collects_multiple_runs():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=1)
    )
    adhd_model = {
        **user_model,
        "attention_stability": attribute(35),
    }

    result = run_simulation_step(
        {
            "user_model": user_model,
            "user_models": {"generic": user_model, "adhd": adhd_model},
            "task_model": task_model,
            "interface_model": interface_model,
            "environment_model": environment_model,
            "computed_parameters": parameters,
            "simulation_model": {},
        }
    )

    assert result["results"]["profile_id"] == "generic"
    assert result["logs"] == result["results"]["timeline"]
    assert result["simulation_results"]["profile_ids"] == [
        "generic",
        "adhd",
    ]


def test_frontend_profile_view_keeps_single_result_unchanged():
    single_result = run_time_discrete_simulation(
        *simulation_inputs(duration_seconds=1)
    )

    assert build_profile_result_views(single_result) == []
    assert build_timeline_rows(single_result["timeline"])


def test_frontend_profile_view_accepts_multi_profile_result():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=1)
    )
    multi_result = simulate_many(
        user_models={"generic": user_model, "adhd": user_model},
        task_model=task_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=parameters,
        profile_labels={"generic": "Generic", "adhd": "ADHD"},
        baseline_profile_id="generic",
    )

    views = build_profile_result_views(
        {"simulation_results": multi_result}
    )

    assert [view["profile_label"] for view in views] == ["Generic", "ADHD"]
    assert views[0]["is_baseline"] is True
    assert views[1]["is_baseline"] is False
    assert views[0]["timeline"]

    rows = build_simulation_table_rows({"simulation_results": multi_result})
    assert {row["Profile ID"] for row in rows} == {"generic", "adhd"}
    assert all("Reading Speed" in row for row in rows)
    assert all("Task Success Score" in row for row in rows)


def test_simulation_table_and_export_include_profile_events():
    logs = [
        {
            "timestamp": "00:01",
            "timestamp_seconds": 1,
            "current_task_step": {"name": "Hinweise lesen"},
            "reading_speed": 42.0,
            "attention": 35.0,
            "fatigue": 20.0,
            "cognitive_load": 75.0,
            "error_risk": 65.0,
            "task_success_score": 40.0,
            "completion_efficiency": 39.0,
            "events": [{"event_type": "very_low_attention"}],
        }
    ]

    rows = build_timeline_rows(logs, "adhd", "ADHD")
    exported = build_simulation_csv(rows)

    assert rows[0]["Profile ID"] == "adhd"
    assert rows[0]["Events"] == "Reduzierte Aufmerksamkeit"
    assert "Profile ID" in exported
    assert "Reduzierte Aufmerksamkeit" in exported


def test_computed_parameters_are_prepared_for_result_display():
    rows = build_computed_parameter_rows(
        {
            "text_complexity": {"value": 62.5},
            "navigation_effort": 48.0,
        }
    )

    assert rows == [
        {"Parameter": "Textschwierigkeit", "Wert": 62.5},
        {"Parameter": "Navigationsaufwand", "Wert": 48.0},
    ]


def test_export_keeps_all_profile_models_and_new_architecture_layers():
    workflow_state = {
        "user_models": {
            "generic": {
                "user_type": "Generic",
                "reading_difficulty": {"value": 10},
                "assumptions": ["Generisches Vergleichsprofil."],
            },
            "adhd": {
                "user_type": "ADHS",
                "reading_difficulty": {"value": 20},
                "assumptions": ["ADHS-Profil."],
            },
        },
        "simulation_plan": {
            "selected_user_profiles": [
                {"profile_id": "generic", "label": "Generic"},
                {"profile_id": "adhd", "label": "ADHS"},
            ]
        },
        "task_model": {"task_name": "Anmeldung"},
        "interface_model": {"text_volume": {"value": 30}},
        "environment_model": {"noise_level": {"value": 20}},
        "computed_parameters": {"text_complexity": {"value": 25}},
    }

    exported = build_simulation_export({}, workflow_state)

    assert [model["profile_id"] for model in exported["user_models"]] == [
        "generic",
        "adhd",
    ]
    assert exported["user_models"][1]["profile_label"] == "ADHS"
    assert exported["user_models"][0]["assumptions"] == [
        "Generisches Vergleichsprofil."
    ]
    assert exported["computed_parameters"]["text_complexity"]["value"] == 25
    assert "combined_model" not in exported
    assert "metric_model" not in exported


def test_single_profile_table_keeps_profile_and_user_state_values():
    single_result = run_time_discrete_simulation(
        *simulation_inputs(duration_seconds=1)
    )

    rows = build_simulation_table_rows(single_result)

    assert len(rows) == len(single_result["timeline"])
    assert rows[0]["Profile ID"] == "generic"
    assert rows[0]["Reading Speed"] == single_result["timeline"][0][
        "reading_speed"
    ]


def test_computed_task_parameters_follow_document_examples():
    interface_model = {
        "sentence_length": attribute(80),
        "word_difficulty": attribute(60),
        "technical_terms": attribute(40),
        "text_volume": attribute(20),
        "navigation_complexity": attribute(70),
        "visual_clutter": attribute(50),
    }
    task_model = {"number_of_steps": attribute(40)}

    assert calculate_text_complexity(interface_model) == 50.0
    assert calculate_navigation_effort(task_model, interface_model) == 53.33

    assert calculate_text_complexity(
        interface_model,
        weights=(1.0, 0.0, 0.0, 0.0),
    ) == 80.0


def test_weights_and_outputs_are_validated_and_clamped():
    with pytest.raises(ValueError, match="sum to 1"):
        validated_weights((0.2, 0.2), 2)

    config = SimulationConfig()
    attention_decay = calculate_attention_decay(
        {
            "distraction_sensitivity": attribute(100),
        },
        {"accessibility_support": attribute(0)},
        {
            "distractions": attribute(100),
            "time_pressure": attribute(100),
            "context_stability": attribute(0),
        },
        fatigue=100,
        config=config,
    )
    attention = update_attention(
        0,
        {"distraction_sensitivity": attribute(100)},
        {"accessibility_support": attribute(0)},
        {
            "distractions": attribute(100),
            "time_pressure": attribute(100),
            "context_stability": attribute(0),
        },
        100,
        config,
    )
    reading_speed = calculate_reading_speed(
        {"reading_difficulty": attribute(0)},
        {"accessibility_support": attribute(100)},
        {"noise_level": attribute(0)},
        {"text_complexity": 0},
    )

    assert attention_decay > 0
    assert attention == 0.0
    assert reading_speed == 100.0


def test_higher_reading_difficulty_reduces_reading_speed():
    generic_user = {
        "user_type": "Generisch",
        "reading_difficulty": attribute(30),
    }
    dyslexia_user = {
        "user_type": "Dyslexie",
        "reading_difficulty": attribute(80),
    }
    interface_model = {"accessibility_support": attribute(20)}
    environment_model = {"noise_level": attribute(40)}
    parameters = {"text_complexity": 50.0}
    generic_speed = calculate_reading_speed(
        generic_user,
        interface_model,
        environment_model,
        parameters,
    )
    dyslexia_speed = calculate_reading_speed(
        dyslexia_user,
        interface_model,
        environment_model,
        parameters,
    )

    assert generic_speed == 75.0
    assert dyslexia_speed == 62.5


def test_dyslexia_reading_load_reduces_reading_speed_for_vulnerable_profile():
    generic_user = {
        "reading_difficulty": attribute(30),
        "sublexical_decoding_stability": attribute(85),
        "orthographic_processing_stability": attribute(85),
        "parallel_letter_processing_stability": attribute(85),
    }
    dyslexie_user = {
        "reading_difficulty": attribute(30),
        "sublexical_decoding_stability": attribute(35),
        "orthographic_processing_stability": attribute(40),
        "parallel_letter_processing_stability": attribute(45),
    }
    interface_model = {"accessibility_support": attribute(20)}
    environment_model = {"noise_level": attribute(20)}
    parameters = {
        "text_complexity": 50.0,
        "dyslexia_reading_load": 80.0,
    }

    generic_speed = calculate_reading_speed(
        generic_user,
        interface_model,
        environment_model,
        parameters,
    )
    dyslexie_speed = calculate_reading_speed(
        dyslexie_user,
        interface_model,
        environment_model,
        parameters,
    )

    assert dyslexie_speed < generic_speed


def test_dyslexia_reading_load_slows_reading_step_progress():
    task_step = {"step_type": "read"}
    user_state = {"reading_speed": 60, "attention": 80, "fatigue": 20}
    result_metrics = {
        "cognitive_load": 40,
        "error_risk": 30,
        "task_success_score": 70,
        "completion_efficiency": 65,
    }

    normal_rate = calculate_task_progress_rate(
        task_step,
        user_state,
        result_metrics,
        navigation_effort=20,
        dyslexia_reading_load=0,
    )
    high_load_rate = calculate_task_progress_rate(
        task_step,
        user_state,
        result_metrics,
        navigation_effort=20,
        dyslexia_reading_load=80,
    )

    assert high_load_rate < normal_rate


def test_linear_user_state_and_result_metrics_follow_document_examples():
    user_model = {
        "reading_difficulty": attribute(60),
        "attention_stability": attribute(80),
        "distraction_sensitivity": attribute(30),
    }
    task_model = {
        "task_complexity": attribute(80),
        "reading_demand": attribute(50),
        "input_demand": attribute(40),
        "memory_demand": attribute(50),
    }
    interface_model = {"accessibility_support": attribute(20)}
    attention_interface_model = {"accessibility_support": attribute(50)}
    environment_model = {
        "noise_level": attribute(40),
        "context_stability": attribute(70),
        "distractions": attribute(20),
        "time_pressure": attribute(60),
    }
    parameters = {"text_complexity": 50.0, "navigation_effort": 53.0}

    reading_speed = calculate_reading_speed(
        user_model,
        interface_model,
        environment_model,
        parameters,
    )
    config = SimulationConfig()
    attention = update_attention(
        80,
        user_model,
        attention_interface_model,
        environment_model,
        10,
        config,
    )
    fatigue = calculate_fatigue_target(task_model, environment_model, attention)
    metrics = calculate_result_metrics(
        task_model,
        environment_model,
        parameters,
        {
            "reading_speed": reading_speed,
            "attention": attention,
            "fatigue": fatigue,
        },
    )

    assert reading_speed == 67.5
    assert attention == 80.0
    assert fatigue == 50.0
    assert metrics["cognitive_load"] == pytest.approx(56.6)
    assert metrics["error_risk"] == pytest.approx(46.65)
    assert metrics["task_success_score"] == pytest.approx(71.35)
    assert metrics["completion_efficiency"] == pytest.approx(72.95)


def test_simulation_uses_hta_order_and_goms_durations():
    user_model = {
        "reading_difficulty": attribute(60),
        "attention_stability": attribute(80),
        "distraction_sensitivity": attribute(30),
    }
    task_model = {
        "task_complexity": attribute(80),
        "number_of_steps": attribute(40),
        "reading_demand": attribute(50),
        "input_demand": attribute(40),
        "memory_demand": attribute(50),
        "steps": [
            {
                "step_id": "step_1",
                "name": "Informationen lesen",
                "goal": "Informationen verstehen",
                "step_type": "read",
                "description": "Hinweise lesen",
                "goms_operations": ["read", "think"],
                "estimated_duration_seconds": 2,
            },
            {
                "step_id": "step_2",
                "name": "Eingaben vornehmen",
                "goal": "Formular ausfüllen",
                "step_type": "input",
                "description": "Werte eingeben",
                "goms_operations": ["point", "click", "type"],
                "estimated_duration_seconds": 3,
            },
        ],
    }
    interface_model = {
        "text_volume": attribute(20),
        "sentence_length": attribute(80),
        "word_difficulty": attribute(60),
        "technical_terms": attribute(40),
        "visual_clutter": attribute(50),
        "navigation_complexity": attribute(70),
        "accessibility_support": attribute(20),
    }
    environment_model = {
        "noise_level": attribute(40),
        "distractions": attribute(20),
        "time_pressure": attribute(60),
        "context_stability": attribute(70),
    }
    computed_task_parameters = {
        "text_complexity": {"value": 50},
        "navigation_effort": {"value": 53},
    }
    config = SimulationConfig(
        event_thresholds={
            "high_error_risk": 0,
            "very_high_cognitive_load": 101,
            "very_low_attention": -1,
        }
    )

    result = run_time_discrete_simulation(
        user_model,
        task_model,
        interface_model,
        environment_model,
        computed_task_parameters,
        config,
    )
    timeline = result["timeline"]

    assert result["total_duration_seconds"] > 5
    assert result["total_task_steps"] == 2
    assert timeline[0]["current_task_step"]["name"] == "Informationen lesen"
    assert timeline[-1]["current_task_step"]["name"] == "Eingaben vornehmen"
    assert timeline[-1]["task_progress"] == 1
    assert [step["base_step_duration"] for step in result["task_step_durations"]] == [
        2,
        3,
    ]
    assert timeline[0]["reading_speed"] < 67.5
    assert timeline[-1]["reading_speed"] < timeline[0]["reading_speed"]
    assert 0 < timeline[0]["attention"] < 80
    assert timeline[-1]["attention"] < timeline[0]["attention"]
    assert timeline[-1]["fatigue"] > timeline[0]["fatigue"]
    assert timeline[0]["input_factors"] == {
        "user_profile": "generic",
        "reading_difficulty": 60.0,
        "text_complexity": 50.0,
        "noise_level": 40.0,
        "accessibility_support": 20.0,
        "attention_stability": 80.0,
        "context_stability": 70.0,
        "distraction_sensitivity": 30.0,
        "distractions": 20.0,
        "task_complexity": 80.0,
        "time_pressure": 60.0,
        "reading_demand": 50.0,
        "input_demand": 40.0,
        "memory_demand": 50.0,
        "navigation_effort": 53.0,
    }
    assert list(build_timeline_rows(timeline)[0]) == [
        "Profile Label",
        "Profile ID",
        "Time",
        "Task Step",
        "Task Progress (%)",
        "Completion Time (s)",
        "Reading Speed",
        "Attention",
        "Fatigue",
        "Cognitive Load",
        "Error Risk Score",
        "Task Success Score",
        "Completion Efficiency",
        "Events",
    ]
    assert timeline[0]["events"][0]["event_type"] == "high_error_risk"
    assert sum(
        event["event_type"] == "high_error_risk"
        for item in timeline
        for event in item["events"]
    ) == 1
    assert set(result["final_metrics"]) == {
        "cognitive_load",
        "error_risk",
        "task_success_score",
        "completion_efficiency",
        "completion_time",
        "time_limit_risk",
    }


def test_reading_speed_decreases_as_fatigue_rises():
    result = run_time_discrete_simulation(
        *simulation_inputs(duration_seconds=20)
    )
    timeline = result["timeline"]

    assert timeline[-1]["fatigue"] > timeline[0]["fatigue"]
    assert timeline[-1]["reading_speed"] < timeline[0]["reading_speed"]


def test_critical_events_are_logged_and_have_state_and_time_effects():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=5)
    )
    task_model["steps"][0]["step_type"] = "input"
    config = SimulationConfig(
        event_thresholds={
            "high_error_risk": 0,
            "very_high_cognitive_load": 0,
            "very_low_attention": 100,
            "time_pressure_warning": 100,
            "rework_error_risk": 0,
        }
    )

    result = run_time_discrete_simulation(
        user_model,
        task_model,
        interface_model,
        environment_model,
        parameters,
        config,
    )
    first_events = result["timeline"][0]["events"]
    event_types = {event["event_type"] for event in first_events}

    assert {
        "high_error_risk",
        "very_high_cognitive_load",
        "very_low_attention",
        "time_pressure_warning",
        "rework_event",
    } <= event_types
    assert all("impact" in event for event in first_events)
    assert result["total_duration_seconds"] > 5
    assert result["timeline"][0]["current_task_step"][
        "effective_duration_seconds"
    ] > 5


def test_multiple_profiles_create_distinct_dynamic_trajectories():
    generic, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=9)
    )
    adhd = {
        **generic,
        "attention_stability": attribute(35),
        "distraction_sensitivity": attribute(80),
    }
    dyslexie = {
        **generic,
        "reading_difficulty": attribute(85),
    }

    result = simulate_many(
        user_models={"generic": generic, "adhd": adhd, "dyslexie": dyslexie},
        task_model=task_model,
        interface_model=interface_model,
        environment_model=environment_model,
        computed_task_parameters=parameters,
        profile_labels={"generic": "Generic", "adhd": "ADHS", "dyslexie": "Dyslexie"},
    )
    runs = result["results_by_profile"]

    assert runs["adhd"]["timeline"][0]["attention"] < runs["generic"][
        "timeline"
    ][0]["attention"]
    assert runs["dyslexie"]["timeline"][0]["reading_speed"] < runs["generic"][
        "timeline"
    ][0]["reading_speed"]
    assert runs["dyslexie"]["completion_time"] > runs["generic"]["completion_time"]
    assert runs["adhd"]["completion_time"] > runs["generic"]["completion_time"]
    assert runs["dyslexie"]["timeline"] != runs["generic"]["timeline"]
    assert all(run["timeline"][-1]["task_progress"] == 1 for run in runs.values())
    assert {
        "completion_time",
        "task_step_durations",
        "longest_task_step",
        "slowest_task_step",
        "fastest_task_step",
    } <= runs["generic"].keys()
    assert {
        "profile",
        "current_task_step_label",
        "task_progress",
        "base_step_duration",
        "actual_step_duration",
        "duration_modifier",
    } <= runs["dyslexie"]["timeline"][0].keys()
    assert runs["dyslexie"]["task_step_durations"][0]["actual_step_duration"] > (
        runs["dyslexie"]["task_step_durations"][0]["base_step_duration"]
    )
    assert runs["generic"]["user_model"] == generic
    assert runs["adhd"]["user_model"] == adhd
    assert runs["dyslexie"]["user_model"] == dyslexie


def test_task_abandonment_can_be_enabled_without_affecting_normal_run():
    result = run_time_discrete_simulation(
        *simulation_inputs(duration_seconds=2),
        config=SimulationConfig(
            enable_task_abandonment=True,
            max_step_duration_factor=3.0,
        ),
    )

    assert result["completed"] is True
    assert result["status"] == "completed"
    assert result["abort_reason"] is None
    assert result["aborted_step_id"] is None
    assert not any(event["event_type"] == "task_aborted" for event in result["events"])


def test_slow_profile_abandons_step_at_configured_maximum_duration():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=3)
    )
    user_model.update(
        {
            "reading_difficulty": attribute(100),
            "attention_stability": attribute(10),
            "distraction_sensitivity": attribute(100),
        }
    )
    task_model["steps"].append(
        {
            "step_id": "step_2",
            "name": "Absenden",
            "step_type": "submit",
            "description": "Formular absenden.",
            "estimated_duration_seconds": 1,
        }
    )

    result = run_time_discrete_simulation(
        user_model,
        task_model,
        interface_model,
        environment_model,
        parameters,
        config=SimulationConfig(
            enable_task_abandonment=True,
            max_step_duration_factor=1.0,
        ),
    )

    assert result["completed"] is False
    assert result["status"] == "aborted"
    assert result["abort_reason"] == "maximum_duration_exceeded"
    assert result["aborted_step_id"] == "step_1"
    assert result["aborted_step_name"] == "Hinweise lesen"
    assert result["allowed_step_duration"] == 3
    assert result["actual_step_duration"] == 3
    assert result["timeline"][-1]["task_progress"] < 1
    assert result["timeline"][-1]["step_status"] == "aborted"
    assert result["timeline"][-1]["abort_reason"] == "maximum_duration_exceeded"
    assert result["final_metrics"]["task_success_score"] == 0
    assert result["final_metrics"]["completion_efficiency"] == 0
    aborted_step = result["aborted_steps"][0]
    assert aborted_step["step_id"] == "step_1"
    assert aborted_step["status"] == "aborted"
    assert aborted_step["abort_reason"] == "maximum_duration_exceeded"
    assert aborted_step["estimated_duration_seconds"] == 3
    assert aborted_step["actual_duration_seconds"] == 3
    assert aborted_step["max_duration_seconds"] == 3
    assert aborted_step["final_progress"] < 1
    assert {
        item["current_task_step"]["step_id"]
        for item in result["timeline"]
    } == {"step_1"}
    assert any(
        event["event_type"] == "task_aborted"
        for event in result["timeline"][-1]["events"]
    )
    assert not any(
        event["event_type"] == "task_abandoned"
        for event in result["timeline"][-1]["events"]
    )
    assert not any(
        event["event_type"] == "task_abandoned"
        for event in result["events"]
    )


def test_maximum_step_duration_uses_central_factor_per_base_duration():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs(duration_seconds=4)
    )
    user_model.update(
        {
            "reading_difficulty": attribute(100),
            "attention_stability": attribute(5),
            "distraction_sensitivity": attribute(100),
        }
    )

    result = run_time_discrete_simulation(
        user_model,
        task_model,
        interface_model,
        environment_model,
        parameters,
        config=SimulationConfig(
            enable_task_abandonment=True,
            max_step_duration_factor=1.5,
        ),
    )

    assert result["completed"] is False
    assert result["allowed_step_duration"] == 6
    assert result["actual_step_duration"] == 6
    assert result["aborted_steps"][0]["max_duration_seconds"] == 6


def test_default_abandonment_factor_is_centralized():
    config = SimulationConfig()

    assert config.enable_task_abandonment is True
    assert config.max_step_duration_factor == 3.0


def test_designer_insights_are_derived_from_timeline_events():
    timeline = [
        {
            "attention": 70.0,
            "reading_speed": 60.0,
            "fatigue": 30.0,
            "cognitive_load": 72.0,
            "error_risk": 40.0,
            "task_success_score": 70.0,
            "completion_efficiency": 62.0,
            "current_task_step": {"step_type": "read"},
            "events": [
                {"event_type": "very_high_cognitive_load"},
                {"event_type": "time_pressure_warning"},
            ],
        },
        {
            "attention": 45.0,
            "reading_speed": 55.0,
            "fatigue": 38.0,
            "cognitive_load": 75.0,
            "error_risk": 58.0,
            "task_success_score": 66.0,
            "completion_efficiency": 58.0,
            "current_task_step": {"step_type": "read"},
            "events": [{"event_type": "rework_event"}],
        },
    ]

    problems, recommendations = derive_profile_insights("ADHS", timeline)

    assert any("Lese- oder Prüfschritt" in problem for problem in problems)
    assert any("mentale Belastung" in problem for problem in problems)
    assert "Textinformationen klarer gliedern" in recommendations
    assert "Schritt vereinfachen und klarer strukturieren" in recommendations
