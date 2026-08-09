from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.core.llm.client import (
    generate_environment_model,
    generate_interface_model,
    generate_task_model,
)
from backend.core.logging.workflow_logging import log_duration
from backend.domains.models.services.task_model_revision import (
    merge_task_model_revision,
)
from backend.domains.planning.schemas.simulation_plan import SimulationPlanSchema
from backend.domains.planning.services.simulation_plan import (
    computation_models_from_plan,
    required_attribute_ids_from_plan,
    required_model_types_from_plan,
)
from backend.domains.users.services.user_profiles import generate_user_models_for_plan


BASE_MODEL_GENERATORS = {
    "task_model": generate_task_model,
    "interface_model": generate_interface_model,
    "environment_model": generate_environment_model,
}


def _model_data(model) -> dict:
    if isinstance(model, dict):
        return model
    return model.model_dump()


def _preserve_reviewed_task_steps(
    *,
    generated_task_model: dict,
    current_task_model: dict | None,
) -> dict:
    if not current_task_model or not current_task_model.get("steps"):
        return generated_task_model

    return {
        **generated_task_model,
        "steps": current_task_model["steps"],
    }


def generate_base_models(
    *,
    scenario_context: dict,
    scenario_dimensions: dict,
    revision_instruction: str,
    simulation_plan: SimulationPlanSchema | None,
    current_task_model: dict | None = None,
) -> dict:
    """Generate all scenario-dependent base models required by the plan."""
    required_model_types = required_model_types_from_plan(
        simulation_plan,
        fallback=(
            model_name.removesuffix("_model")
            for model_name in BASE_MODEL_GENERATORS
        ),
    )
    selected_generators = {
        model_name: generator
        for model_name, generator in BASE_MODEL_GENERATORS.items()
        if model_name != "user_model"
        if model_name.removesuffix("_model") in required_model_types
    }
    generated_models: dict = {}

    with log_duration(
        "domain.models.generate_base_models",
        model_count=len(selected_generators),
        required_attributes=required_attribute_ids_from_plan(simulation_plan),
        computation_models=[
            model.model_id
            for model in computation_models_from_plan(simulation_plan)
        ],
    ):
        if selected_generators:
            with ThreadPoolExecutor(max_workers=len(selected_generators)) as executor:
                futures = {
                    executor.submit(
                        generator,
                        scenario_context=scenario_context,
                        scenario_dimensions=scenario_dimensions,
                        revision_instruction=revision_instruction,
                        simulation_plan=simulation_plan,
                    ): model_name
                    for model_name, generator in selected_generators.items()
                }

                for future in as_completed(futures):
                    model_name = futures[future]
                    with log_duration(
                        "domain.models.generate_base_models.collect",
                        model_name=model_name,
                    ):
                        model_data = _model_data(future.result())
                        if model_name == "task_model":
                            model_data = _preserve_reviewed_task_steps(
                                generated_task_model=model_data,
                                current_task_model=current_task_model,
                            )
                        generated_models[model_name] = model_data

    profiled_models = generate_user_models_for_plan(simulation_plan)
    generated_models["user_models"] = {
        profile_id: profiled_model.user_model.model_dump()
        for profile_id, profiled_model in profiled_models.items()
    }
    baseline_profile = next(
        (
            profile
            for profile in profiled_models.values()
            if profile.is_baseline
        ),
        next(iter(profiled_models.values())),
    )
    generated_models["user_model"] = baseline_profile.user_model.model_dump()

    if simulation_plan is not None:
        generated_models["simulation_plan"] = simulation_plan.model_dump()

    return generated_models


def generate_task_model_data(
    *,
    scenario_context: dict,
    scenario_dimensions: dict,
    revision_instruction: str,
    simulation_plan: SimulationPlanSchema | None,
    current_task_model: dict | None = None,
) -> dict:
    task_model = generate_task_model(
        scenario_context=scenario_context,
        scenario_dimensions=scenario_dimensions,
        revision_instruction=revision_instruction,
        simulation_plan=simulation_plan,
        current_task_model=current_task_model,
    )
    task_model_data = task_model.model_dump()
    if current_task_model:
        return merge_task_model_revision(
            current_task_model,
            task_model_data,
        )
    return task_model_data


def generate_interface_model_data(
    *,
    scenario_context: dict,
    scenario_dimensions: dict,
    revision_instruction: str,
    simulation_plan: SimulationPlanSchema | None,
) -> dict:
    return generate_interface_model(
        scenario_context=scenario_context,
        scenario_dimensions=scenario_dimensions,
        revision_instruction=revision_instruction,
        simulation_plan=simulation_plan,
    ).model_dump()


def generate_environment_model_data(
    *,
    scenario_context: dict,
    scenario_dimensions: dict,
    revision_instruction: str,
    simulation_plan: SimulationPlanSchema | None,
) -> dict:
    return generate_environment_model(
        scenario_context=scenario_context,
        scenario_dimensions=scenario_dimensions,
        revision_instruction=revision_instruction,
        simulation_plan=simulation_plan,
    ).model_dump()
