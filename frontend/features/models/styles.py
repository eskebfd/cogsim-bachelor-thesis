from frontend.features.models.style_sections.attributes import MODELS_ATTRIBUTES_CSS
from frontend.features.models.style_sections.intro import MODELS_INTRO_CSS
from frontend.features.models.style_sections.responsive import MODELS_RESPONSIVE_CSS
from frontend.features.models.style_sections.review_cards import MODELS_REVIEW_CARDS_CSS
from frontend.features.models.style_sections.task_flow import MODELS_TASK_FLOW_CSS
from frontend.features.models.style_sections.user_comparison import (
    MODELS_USER_COMPARISON_CSS,
)
from frontend.features.models.style_sections.user_profiles import MODELS_USER_PROFILES_CSS


MODELS_CSS = "".join(
    [
        MODELS_INTRO_CSS,
        MODELS_REVIEW_CARDS_CSS.removeprefix("\n"),
        MODELS_TASK_FLOW_CSS.removeprefix("\n"),
        MODELS_ATTRIBUTES_CSS.removeprefix("\n"),
        MODELS_USER_PROFILES_CSS.removeprefix("\n"),
        MODELS_USER_COMPARISON_CSS.removeprefix("\n"),
        MODELS_RESPONSIVE_CSS.removeprefix("\n"),
    ]
)
