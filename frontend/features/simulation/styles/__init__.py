from frontend.features.simulation.styles.comparison import (
    RESULT_COMPARISON_CSS,
)
from frontend.features.simulation.styles.events import RESULT_EVENTS_CSS
from frontend.features.simulation.styles.insights import RESULT_INSIGHTS_CSS
from frontend.features.simulation.styles.responsive import (
    RESULT_RESPONSIVE_CSS,
)
from frontend.features.simulation.styles.summary import RESULT_SUMMARY_CSS
from frontend.features.simulation.styles.timeline import RESULT_TIMELINE_CSS


SIMULATION_CSS = "\n".join(
    (
        RESULT_TIMELINE_CSS,
        RESULT_SUMMARY_CSS,
        RESULT_COMPARISON_CSS,
        RESULT_EVENTS_CSS,
        RESULT_INSIGHTS_CSS,
        RESULT_RESPONSIVE_CSS,
    )
)
