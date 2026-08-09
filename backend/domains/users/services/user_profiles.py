from backend.domains.planning.schemas.simulation_plan import UserProfileSelection
from backend.domains.planning.schemas.simulation_plan import SimulationPlanSchema
from backend.domains.models.schemas.attribute import AttributeValueSchema
from backend.domains.users.registry import (
    get_baseline_user_profile_id,
    get_user_profile,
    list_user_profiles,
    require_user_profile,
    validate_user_profile_ids,
)
from backend.domains.users.schemas.user_model import ProfiledUserModelSchema, UserModelSchema
from backend.domains.users.schemas.profile_definition import UserProfileDefinition


_ATTRIBUTE_SCALE_DESCRIPTIONS = {
    "reading_difficulty": (
        "Keine Schwierigkeiten beim Lesen",
        "Sehr starke Schwierigkeiten beim Lesen",
    ),
    "sublexical_decoding_stability": (
        "Graphem-Phonem-Zuordnung ist sehr instabil",
        "Graphem-Phonem-Zuordnung bleibt sehr stabil",
    ),
    "orthographic_processing_stability": (
        "Orthografische Wortverarbeitung ist sehr instabil",
        "Orthografische Wortverarbeitung bleibt sehr stabil",
    ),
    "parallel_letter_processing_stability": (
        "Mehrere Buchstaben werden kaum parallel erfasst",
        "Mehrere Buchstaben werden sehr stabil parallel erfasst",
    ),
    "attention_stability": (
        "Aufmerksamkeit ist sehr instabil",
        "Aufmerksamkeit bleibt sehr stabil",
    ),
    "distraction_sensitivity": (
        "Kaum empfindlich gegenüber Ablenkungen",
        "Sehr empfindlich gegenüber Ablenkungen",
    ),
    "task_switching_difficulty": (
        "Aufgabenwechsel fallen sehr leicht",
        "Aufgabenwechsel fallen sehr schwer",
    ),
    "vigilance_stability": (
        "Daueraufmerksamkeit bricht sehr schnell ein",
        "Daueraufmerksamkeit bleibt sehr stabil",
    ),
    "inhibitory_control": (
        "Unpassende Reaktionen werden kaum gehemmt",
        "Unpassende Reaktionen werden sehr stabil gehemmt",
    ),
    "attention_switching_stability": (
        "Aufmerksamkeitswechsel sind sehr instabil",
        "Aufmerksamkeitswechsel bleiben sehr stabil",
    ),
    "divided_attention_capacity": (
        "Mehrere Informationsquellen können kaum parallel beachtet werden",
        "Mehrere Informationsquellen können sehr gut parallel beachtet werden",
    ),
    "omission_tendency": (
        "Sehr geringe Tendenz, relevante Hinweise zu übersehen",
        "Sehr hohe Tendenz, relevante Hinweise oder Schritte zu übersehen",
    ),
    "reaction_variability": (
        "Reaktionen sind sehr gleichmäßig",
        "Reaktionen schwanken sehr stark",
    ),
    "working_memory_stability": (
        "Arbeitsgedächtnis ist sehr instabil",
        "Arbeitsgedächtnis bleibt sehr stabil",
    ),
}

_PROFILE_ASSUMPTIONS = {
    "generic": ["Generisches Vergleichsprofil ohne spezifische Einschränkung."],
    "adhd": [
        "ADHS-Profil mit erhöhter Ablenkungsempfindlichkeit sowie reduzierter Daueraufmerksamkeit, Inhibition und Aufmerksamkeitswechsel-Stabilität."
    ],
    "dyslexie": [
        "Dyslexie-Profil mit deutlich erhöhter Leseschwierigkeit und reduzierter Dekodier-, orthografischer und paralleler Buchstabenverarbeitungsstabilität."
    ],
}


def get_available_user_profiles() -> list[UserProfileDefinition]:
    return list_user_profiles()


def get_user_profile_by_id(profile_id: str) -> UserProfileDefinition | None:
    return get_user_profile(profile_id)


def build_user_profile_selections(
    profile_ids: list[str] | None = None,
) -> list[UserProfileSelection]:
    baseline_profile_id = get_baseline_user_profile_id()
    selected_ids = list(dict.fromkeys(profile_ids or [baseline_profile_id]))
    validate_user_profile_ids(selected_ids)
    if baseline_profile_id not in selected_ids:
        selected_ids.insert(0, baseline_profile_id)

    selections = []
    for profile_id in selected_ids:
        profile = require_user_profile(profile_id)
        selections.append(
            UserProfileSelection(
                profile_id=profile.profile_id,
                label=profile.label,
                is_baseline=profile.is_baseline,
            )
        )
    return selections


def build_user_model_from_profile(profile_id: str) -> UserModelSchema:
    profile = require_user_profile(profile_id)

    attributes = {}
    for attribute_id, profile_attribute in profile.attributes.items():
        minimum, maximum = _ATTRIBUTE_SCALE_DESCRIPTIONS[attribute_id]
        attributes[attribute_id] = AttributeValueSchema(
            value=round(profile_attribute.value),
            scale_min_description=minimum,
            scale_max_description=maximum,
            explanation=(
                f"Fester Registry-Wert für das Profil {profile.label}."
            ),
            confidence="high",
        )

    return UserModelSchema(
        user_type=profile.label,
        **attributes,
        assumptions=list(_PROFILE_ASSUMPTIONS[profile.profile_id]),
    )


def generate_user_models_for_plan(
    simulation_plan: SimulationPlanSchema | None,
    **_ignored,
) -> dict[str, ProfiledUserModelSchema]:
    selections = (
        simulation_plan.selected_user_profiles
        if simulation_plan is not None
        else build_user_profile_selections()
    )
    return {
        selection.profile_id: ProfiledUserModelSchema(
            profile_id=selection.profile_id,
            label=selection.label,
            is_baseline=selection.is_baseline,
            user_model=build_user_model_from_profile(selection.profile_id),
        )
        for selection in selections
    }
