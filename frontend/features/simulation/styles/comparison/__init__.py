from frontend.features.simulation.styles.comparison.core import (
    RESULT_COMPARISON_CORE_CSS,
)
from frontend.features.simulation.styles.comparison.guidance import (
    RESULT_COMPARISON_GUIDANCE_CSS,
)
from frontend.features.simulation.styles.comparison.overview import (
    RESULT_COMPARISON_OVERVIEW_CSS,
)
from frontend.features.simulation.styles.comparison.profile_cards import (
    RESULT_COMPARISON_PROFILE_CARDS_CSS,
)


RESULT_COMPARISON_CSS = "".join(
    [
        RESULT_COMPARISON_CORE_CSS,
        RESULT_COMPARISON_OVERVIEW_CSS.removeprefix("\n"),
        RESULT_COMPARISON_GUIDANCE_CSS.removeprefix("\n"),
        RESULT_COMPARISON_PROFILE_CARDS_CSS.removeprefix("\n"),
    ]
)
