from backend.domains.users.profiles.common import profile_attributes
from backend.domains.users.schemas.profile_definition import UserProfileDefinition


ADHD_PROFILE = UserProfileDefinition(
    profile_id="adhd",
    label="ADHS",
    attributes=profile_attributes(
        {
            "reading_difficulty": 18,
            "sublexical_decoding_stability": 80,
            "orthographic_processing_stability": 80,
            "parallel_letter_processing_stability": 76,
            "attention_stability": 72,
            "distraction_sensitivity": 82,
            "task_switching_difficulty": 72,
            "vigilance_stability": 58,
            "inhibitory_control": 58,
            "attention_switching_stability": 60,
            "divided_attention_capacity": 58,
            "omission_tendency": 62,
            "reaction_variability": 68,
            "working_memory_stability": 58,
        }
    ),
)
