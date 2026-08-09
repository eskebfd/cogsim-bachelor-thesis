from backend.domains.users.profiles.common import profile_attributes
from backend.domains.users.schemas.profile_definition import UserProfileDefinition


GENERIC_PROFILE = UserProfileDefinition(
    profile_id="generic",
    label="Generic",
    is_baseline=True,
    attributes=profile_attributes(
        {
            "reading_difficulty": 10,
            "sublexical_decoding_stability": 86,
            "orthographic_processing_stability": 86,
            "parallel_letter_processing_stability": 84,
            "attention_stability": 85,
            "distraction_sensitivity": 20,
            "task_switching_difficulty": 20,
            "vigilance_stability": 84,
            "inhibitory_control": 84,
            "attention_switching_stability": 82,
            "divided_attention_capacity": 82,
            "omission_tendency": 18,
            "reaction_variability": 18,
            "working_memory_stability": 82,
        }
    ),
)
