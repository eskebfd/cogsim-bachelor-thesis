from backend.domains.users.schemas.profile_definition import (
    UserProfileAttribute,
)


ATTRIBUTE_NAMES = {
    "reading_difficulty": "Reading Difficulty",
    "sublexical_decoding_stability": "Sublexical Decoding Stability",
    "orthographic_processing_stability": "Orthographic Processing Stability",
    "parallel_letter_processing_stability": "Parallel Letter Processing Stability",
    "attention_stability": "Attention Stability",
    "distraction_sensitivity": "Distraction Sensitivity",
    "task_switching_difficulty": "Task Switching Difficulty",
    "vigilance_stability": "Vigilance Stability",
    "inhibitory_control": "Inhibitory Control",
    "attention_switching_stability": "Attention Switching Stability",
    "divided_attention_capacity": "Divided Attention Capacity",
    "omission_tendency": "Omission Tendency",
    "reaction_variability": "Reaction Variability",
    "working_memory_stability": "Working Memory Stability",
}


def profile_attributes(
    values: dict[str, float],
) -> dict[str, UserProfileAttribute]:
    return {
        attribute_id: UserProfileAttribute(
            attribute_id=attribute_id,
            name=ATTRIBUTE_NAMES[attribute_id],
            value=value,
        )
        for attribute_id, value in values.items()
    }
