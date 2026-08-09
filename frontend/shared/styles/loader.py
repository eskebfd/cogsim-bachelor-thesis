from frontend.shared.styles.base import BASE_CSS
from frontend.shared.styles.components.buttons import BUTTONS_CSS
from frontend.shared.styles.components.cards import CARDS_CSS
from frontend.shared.styles.components.data_display import DATA_DISPLAY_CSS
from frontend.shared.styles.components.forms import FORMS_CSS
from frontend.shared.styles.components.loading_overlay import LOADING_OVERLAY_CSS
from frontend.workflow.styles import TIMELINE_CSS
from frontend.shared.styles.layout import LAYOUT_CSS
from frontend.features.computed_parameters.styles import COMPUTED_PARAMETERS_CSS
from frontend.features.dimensions.styles import DIMENSIONS_CSS
from frontend.features.evaluation_goals.styles import EVALUATION_GOALS_CSS
from frontend.features.home.styles import HOME_CSS
from frontend.features.models.styles import MODELS_CSS
from frontend.features.scenario.styles import SCENARIO_CSS
from frontend.features.simulation.styles import SIMULATION_CSS
from frontend.features.user_profiles.styles import USER_PROFILES_CSS
from frontend.shared.styles.tokens import build_background_css, build_token_css
from frontend.shared.styles.components.sidebar import SIDEBAR_CSS


STEP_STYLES = [
    HOME_CSS,
    USER_PROFILES_CSS,
    SCENARIO_CSS,
    DIMENSIONS_CSS,
    EVALUATION_GOALS_CSS,
    MODELS_CSS,
    COMPUTED_PARAMETERS_CSS,
    SIMULATION_CSS,
]


def build_cogsim_css() -> str:
    sections = [
        build_token_css(),
        BASE_CSS,
        build_background_css(),
        LAYOUT_CSS,
        CARDS_CSS,
        BUTTONS_CSS,
        TIMELINE_CSS,
        DATA_DISPLAY_CSS,
        FORMS_CSS,
        LOADING_OVERLAY_CSS,
        SIDEBAR_CSS,
        *STEP_STYLES,
    ]

    return "<style>\n" + "\n".join(sections) + "\n</style>"
