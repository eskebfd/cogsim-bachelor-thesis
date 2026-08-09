import copy

import pytest

from backend.domains.simulation.algorithms.registry import (
    SimulationAlgorithmRegistry,
    calculate_with_algorithm,
)
from backend.domains.simulation.config import SimulationConfig
from backend.domains.simulation.engine import run_time_discrete_simulation
from backend.domains.simulation.engine import calculate_task_progress_rate
from backend.domains.simulation.events import event_conditions
from backend.domains.simulation.events.registry import SimulationEventRegistry
from backend.domains.simulation.metrics import (
    calculate_cognitive_load,
    calculate_error_risk,
    calculate_result_metrics,
)
from backend.domains.simulation.algorithms.state_updates import calculate_attention_decay
from backend.domains.simulation.metrics.registry import (
    SimulationMetricRegistry,
    calculate_metric,
)
from backend.domains.users.registry import UserProfileRegistry
from backend.domains.users.schemas.profile_definition import (
    UserProfileAttribute,
    UserProfileDefinition,
)
from backend.domains.users.services.user_profiles import (
    build_user_model_from_profile,
    get_available_user_profiles,
)


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


def test_profile_registry_exposes_existing_profiles_with_same_values():
    profiles = get_available_user_profiles()

    assert [profile.profile_id for profile in profiles] == [
        "generic",
        "adhd",
        "dyslexie",
    ]
    assert build_user_model_from_profile("generic").attention_stability.value == 85
    assert build_user_model_from_profile("adhd").attention_stability.value == 72
    assert build_user_model_from_profile("dyslexie").reading_difficulty.value == 82
    assert (
        build_user_model_from_profile("dyslexie").sublexical_decoding_stability.value
        == 38
    )


def test_profile_initial_attention_starts_above_low_attention_event_threshold():
    config = SimulationConfig()
    threshold = config.event_thresholds["very_low_attention"]

    for profile_id in ("generic", "adhd", "dyslexie"):
        user_model = build_user_model_from_profile(profile_id).model_dump()
        assert user_model["attention_stability"]["value"] > threshold


def test_profile_registry_rejects_unknown_and_duplicate_ids():
    registry = UserProfileRegistry()
    profile = UserProfileDefinition(
        profile_id="test",
        label="Test",
        is_baseline=True,
        attributes={
            "reading_difficulty": UserProfileAttribute(
                attribute_id="reading_difficulty",
                name="Reading Difficulty",
                value=10,
            )
        },
    )

    registry.register(profile)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(profile)
    with pytest.raises(ValueError, match="Unknown user profile ID"):
        registry.require("missing")
    assert registry.baseline().profile_id == "test"


def test_new_test_profile_can_be_registered_in_isolated_registry():
    registry = UserProfileRegistry()
    profile = UserProfileDefinition(
        profile_id="research_test",
        label="Research Test",
        attributes={
            "reading_difficulty": UserProfileAttribute(
                attribute_id="reading_difficulty",
                name="Reading Difficulty",
                value=42,
            )
        },
    )

    registry.register(profile, baseline=True)

    assert registry.get("research_test").attributes["reading_difficulty"].value == 42


def test_algorithm_registry_rejects_unknown_and_duplicate_ids():
    class TestAlgorithm:
        algorithm_id = "test.algorithm"

        def calculate(self, **kwargs):
            return kwargs["value"] + 1

    registry = SimulationAlgorithmRegistry()
    algorithm = TestAlgorithm()

    registry.register(algorithm)

    assert registry.get("test.algorithm").calculate(value=1) == 2
    with pytest.raises(ValueError, match="already registered"):
        registry.register(algorithm)
    with pytest.raises(ValueError, match="Unknown simulation algorithm ID"):
        registry.get("missing.algorithm")


def test_registered_algorithms_match_existing_public_facades():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs()
    )
    user_state = {"reading_speed": 50, "attention": 70, "fatigue": 20}
    config = SimulationConfig()

    assert calculate_with_algorithm(
        "attention.linear_decay",
        user_model=user_model,
        interface_model=interface_model,
        environment_model=environment_model,
        fatigue=user_state["fatigue"],
        config=config,
    ) == calculate_attention_decay(
        user_model,
        interface_model,
        environment_model,
        user_state["fatigue"],
        config,
    )
    metrics = {
        "cognitive_load": 50,
        "error_risk": 40,
        "task_success_score": 70,
        "completion_efficiency": 60,
    }
    assert calculate_with_algorithm(
        "progress.slowdown",
        task_step=task_model["steps"][0],
        user_state=user_state,
        result_metrics=metrics,
        navigation_effort=parameters["navigation_effort"]["value"],
    ) == calculate_task_progress_rate(
        task_model["steps"][0],
        user_state,
        metrics,
        parameters["navigation_effort"]["value"],
    )


def test_metric_registry_rejects_unknown_and_duplicate_ids():
    class TestMetric:
        metric_id = "test_metric"

        def calculate(self, **kwargs):
            return kwargs["value"] * 2

    registry = SimulationMetricRegistry()
    metric = TestMetric()

    registry.register(metric)

    assert registry.get("test_metric").calculate(value=3) == 6
    with pytest.raises(ValueError, match="already registered"):
        registry.register(metric)
    with pytest.raises(ValueError, match="Unknown simulation metric ID"):
        registry.get("missing_metric")


def test_registered_metrics_match_existing_public_facades():
    user_model, task_model, interface_model, environment_model, parameters = (
        simulation_inputs()
    )
    user_state = {"reading_speed": 50, "attention": 70, "fatigue": 20}
    flat_parameters = {"text_complexity": 50, "navigation_effort": 30}

    cognitive_load = calculate_cognitive_load(
        task_model,
        flat_parameters,
        user_state,
    )
    error_risk = calculate_error_risk(
        cognitive_load,
        user_state,
        environment_model,
    )

    assert cognitive_load == calculate_metric(
        "cognitive_load",
        task_model=task_model,
        computed_task_parameters=flat_parameters,
        user_state=user_state,
    )
    assert error_risk == calculate_metric(
        "error_risk",
        cognitive_load=cognitive_load,
        user_state=user_state,
        environment_model=environment_model,
    )
    assert calculate_result_metrics(
        task_model,
        environment_model,
        flat_parameters,
        user_state,
    ) == {
        "cognitive_load": cognitive_load,
        "error_risk": error_risk,
        "task_success_score": calculate_metric(
            "task_success_score",
            error_risk=error_risk,
            cognitive_load=cognitive_load,
            computed_task_parameters=flat_parameters,
        ),
        "completion_efficiency": calculate_metric(
            "completion_efficiency",
            user_state=user_state,
            task_success_score=calculate_metric(
                "task_success_score",
                error_risk=error_risk,
                cognitive_load=cognitive_load,
                computed_task_parameters=flat_parameters,
            ),
        ),
    }


def test_legacy_task_success_probability_metric_id_calculates_score():
    computed_parameters = {"navigation_effort": 40}

    legacy_value = calculate_metric(
        "task_success_probability",
        error_risk=35,
        cognitive_load=50,
        computed_task_parameters=computed_parameters,
    )
    canonical_value = calculate_metric(
        "task_success_score",
        error_risk=35,
        cognitive_load=50,
        computed_task_parameters=computed_parameters,
    )

    assert legacy_value == canonical_value


def test_event_registry_rejects_unknown_and_duplicate_types():
    class TestEvent:
        event_type = "test_event"

        def condition(self, **kwargs):
            return {
                "active": True,
                "value": 1,
                "threshold": 1,
                "message": "Test",
            }

        def effect(self, **kwargs):
            return {
                "attention_change": 0.0,
                "fatigue_change": 0.0,
                "additional_seconds": 0,
            }

    registry = SimulationEventRegistry()
    event = TestEvent()

    registry.register(event)

    assert registry.get("test_event").condition()["active"] is True
    with pytest.raises(ValueError, match="already registered"):
        registry.register(event)
    with pytest.raises(ValueError, match="Unknown simulation event type"):
        registry.get("missing_event")


def test_registered_events_keep_existing_trigger_values():
    config = SimulationConfig()
    conditions = event_conditions(
        {"reading_speed": 50, "attention": 60, "fatigue": 20},
        {
            "cognitive_load": 70,
            "error_risk": 65,
            "task_success_score": 70,
            "completion_efficiency": 60,
        },
        config,
        elapsed_seconds=90,
        time_limit_seconds=100,
        task_step={"step_type": "input"},
        rework_allowed=True,
        abandonment_enabled=True,
        abandonment_allowed=True,
        elapsed_step_seconds=6,
        max_step_duration=6,
    )

    assert conditions["high_error_risk"]["active"] is True
    assert conditions["very_high_cognitive_load"]["active"] is True
    assert conditions["very_low_attention"]["active"] is True
    assert conditions["time_pressure_warning"]["active"] is True
    assert conditions["rework_event"]["active"] is True
    assert conditions["task_aborted"]["active"] is True


def test_profile_specific_aggregate_load_events_are_not_registered():
    config = SimulationConfig()
    metrics = {
        "cognitive_load": 30,
        "error_risk": 30,
        "task_success_score": 80,
        "completion_efficiency": 75,
    }

    conditions = event_conditions(
        {"reading_speed": 55, "attention": 80, "fatigue": 20},
        metrics,
        config,
        task_step={"step_type": "read"},
        computed_task_parameters={
            "dyslexia_reading_load": 80,
            "adhd_interaction_load": 75,
        },
    )

    assert "high_dyslexia_reading_load" not in conditions
    assert "attention_lapse" not in conditions


def test_adhd_load_events_trigger_from_computed_parameters():
    config = SimulationConfig()
    metrics = {
        "cognitive_load": 55,
        "error_risk": 45,
        "task_success_score": 70,
        "completion_efficiency": 65,
    }

    conditions = event_conditions(
        {"reading_speed": 65, "attention": 55, "fatigue": 30},
        metrics,
        config,
        task_step={"step_type": "select"},
        computed_task_parameters={
            "adhd_interaction_load": 75,
            "inhibition_load": 80,
            "attention_switching_load": 78,
        },
    )

    assert conditions["high_inhibition_load"]["active"] is True
    assert conditions["task_switching_strain"]["active"] is True


def test_engine_results_and_events_are_deterministic_with_registries():
    inputs = simulation_inputs(duration_seconds=5)
    config = SimulationConfig(
        state_response_rates={"attention": 0.0, "fatigue": 0.1},
        event_thresholds={
            "high_error_risk": 70,
            "very_high_cognitive_load": 80,
            "very_low_attention": 15,
        },
    )

    first = run_time_discrete_simulation(*copy.deepcopy(inputs), config=config)
    second = run_time_discrete_simulation(*copy.deepcopy(inputs), config=config)

    assert first["final_metrics"] == second["final_metrics"]
    assert first["completion_time"] == second["completion_time"]
    assert [
        (event["event_type"], event["timestamp_seconds"])
        for event in first["events"]
    ] == [
        (event["event_type"], event["timestamp_seconds"])
        for event in second["events"]
    ]
