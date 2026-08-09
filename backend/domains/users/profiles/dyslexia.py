from backend.domains.users.profiles.common import profile_attributes
from backend.domains.users.schemas.profile_definition import UserProfileDefinition


DYSLEXIA_PROFILE = UserProfileDefinition(
    profile_id="dyslexie",
    label="Dyslexie",
    attributes=profile_attributes(
        {
            "reading_difficulty": 82,
            "sublexical_decoding_stability": 38,
            "orthographic_processing_stability": 42,
            "parallel_letter_processing_stability": 45,
            "attention_stability": 78,
            "distraction_sensitivity": 32,
            "task_switching_difficulty": 35,
            "vigilance_stability": 76,
            "inhibitory_control": 78,
            "attention_switching_stability": 74,
            "divided_attention_capacity": 72,
            "omission_tendency": 28,
            "reaction_variability": 28,
            "working_memory_stability": 66,
        }
    ),
)
