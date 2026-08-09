import pytest

from backend.domains.evaluation.registries.metrics import get_metric_by_id
from backend.domains.planning.services.simulation_plan import (
    build_simulation_plan_for_profile_ids,
)
from backend.domains.users.services.user_profiles import (
    build_user_profile_selections,
    build_user_model_from_profile,
    generate_user_models_for_plan,
    get_available_user_profiles,
    get_user_profile_by_id,
)


def test_available_profiles_include_generic_adhd_and_dyslexie():
    profiles = get_available_user_profiles()

    assert [profile.profile_id for profile in profiles] == [
        "generic",
        "adhd",
        "dyslexie",
    ]


def test_all_profiles_have_the_same_attribute_ids():
    profiles = get_available_user_profiles()
    attribute_sets = [set(profile.attributes) for profile in profiles]

    assert all(attributes == attribute_sets[0] for attributes in attribute_sets)
    assert attribute_sets[0] == {
        "reading_difficulty",
        "sublexical_decoding_stability",
        "orthographic_processing_stability",
        "parallel_letter_processing_stability",
        "attention_stability",
        "distraction_sensitivity",
        "task_switching_difficulty",
        "vigilance_stability",
        "inhibitory_control",
        "attention_switching_stability",
        "divided_attention_capacity",
        "omission_tendency",
        "reaction_variability",
        "working_memory_stability",
    }


def test_all_profile_values_are_between_zero_and_one_hundred():
    profiles = get_available_user_profiles()

    assert all(
        0 <= attribute.value <= 100
        for profile in profiles
        for attribute in profile.attributes.values()
    )


def test_profile_lookup_returns_a_copy_or_none():
    profile = get_user_profile_by_id("dyslexie")

    assert profile is not None
    assert profile.attributes["reading_difficulty"].value == 82
    assert get_user_profile_by_id("unknown_profile") is None


def test_adhd_selection_adds_generic_baseline():
    selections = build_user_profile_selections(["adhd"])

    assert [selection.profile_id for selection in selections] == [
        "generic",
        "adhd",
    ]
    assert selections[0].is_baseline is True


def test_generic_and_dyslexie_selection_is_preserved():
    selections = build_user_profile_selections(["generic", "dyslexie"])

    assert [selection.profile_id for selection in selections] == [
        "generic",
        "dyslexie",
    ]


def test_unknown_profile_is_rejected():
    with pytest.raises(ValueError, match="unknown_profile"):
        build_user_profile_selections(["unknown_profile"])


def test_simulation_plan_accepts_registry_profile_selections():
    metric = get_metric_by_id("cognitive_load")
    assert metric is not None

    plan = build_simulation_plan_for_profile_ids(["adhd"], [metric])

    assert [profile.profile_id for profile in plan.selected_user_profiles] == [
        "generic",
        "adhd",
    ]
    assert plan.selected_user_profiles[0].is_baseline is True


def test_multiple_profile_user_models_keep_profile_ids():
    metric = get_metric_by_id("cognitive_load")
    assert metric is not None
    plan = build_simulation_plan_for_profile_ids(["adhd"], [metric])
    generated = generate_user_models_for_plan(
        simulation_plan=plan,
    )

    assert list(generated) == ["generic", "adhd"]
    assert generated["generic"].is_baseline is True
    assert generated["adhd"].profile_id == "adhd"
    assert generated["generic"].user_model.user_type == "Generic"
    assert generated["adhd"].user_model.user_type == "ADHS"


def test_single_profile_also_creates_a_profiled_user_model():
    metric = get_metric_by_id("cognitive_load")
    assert metric is not None
    plan = build_simulation_plan_for_profile_ids(["generic"], [metric])

    generated = generate_user_models_for_plan(simulation_plan=plan)

    assert list(generated) == ["generic"]
    assert generated["generic"].is_baseline is True


def test_all_registry_user_models_share_schema_and_differ_by_profile():
    models = {
        profile_id: build_user_model_from_profile(profile_id)
        for profile_id in ("generic", "adhd", "dyslexie")
    }
    attribute_ids = {
        "reading_difficulty",
        "attention_stability",
        "distraction_sensitivity",
        "task_switching_difficulty",
        "working_memory_stability",
    }

    for model in models.values():
        assert attribute_ids.issubset(model.model_fields_set)
    assert models["adhd"].attention_stability.value != (
        models["generic"].attention_stability.value
    )
    assert models["dyslexie"].reading_difficulty.value != (
        models["generic"].reading_difficulty.value
    )


def test_profile_assumptions_are_not_mixed():
    generic = build_user_model_from_profile("generic")
    adhd = build_user_model_from_profile("adhd")
    dyslexie = build_user_model_from_profile("dyslexie")

    generic_text = " ".join(generic.assumptions).lower()
    assert "adhs" not in generic_text
    assert "dyslexie" not in generic_text
    assert "adhs" in " ".join(adhd.assumptions).lower()
    assert "dyslexie" in " ".join(dyslexie.assumptions).lower()


def test_three_selected_profiles_create_three_user_models():
    metric = get_metric_by_id("cognitive_load")
    assert metric is not None
    plan = build_simulation_plan_for_profile_ids(
        ["generic", "adhd", "dyslexie"], [metric]
    )

    generated = generate_user_models_for_plan(plan)

    assert list(generated) == ["generic", "adhd", "dyslexie"]
