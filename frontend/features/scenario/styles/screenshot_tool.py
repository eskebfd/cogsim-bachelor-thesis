from frontend.features.scenario.styles.screenshot_tool_sections.attachment import (
    SCREENSHOT_ATTACHMENT_CSS,
)
from frontend.features.scenario.styles.screenshot_tool_sections.capture import (
    SCREENSHOT_CAPTURE_CSS,
)
from frontend.features.scenario.styles.screenshot_tool_sections.editor import (
    SCREENSHOT_EDITOR_CSS,
)
from frontend.features.scenario.styles.screenshot_tool_sections.responsive import (
    SCREENSHOT_RESPONSIVE_CSS,
)
from frontend.features.scenario.styles.screenshot_tool_sections.status import (
    SCREENSHOT_STATUS_CSS,
)
from frontend.features.scenario.styles.screenshot_tool_sections.summary import (
    SCREENSHOT_SUMMARY_CSS,
)
from frontend.features.scenario.styles.screenshot_tool_sections.tool_panel import (
    SCREENSHOT_TOOL_PANEL_CSS,
)


SCREENSHOT_TOOL_CSS = "".join(
    [
        SCREENSHOT_ATTACHMENT_CSS,
        SCREENSHOT_CAPTURE_CSS.removeprefix("\n"),
        SCREENSHOT_STATUS_CSS.removeprefix("\n"),
        SCREENSHOT_SUMMARY_CSS.removeprefix("\n"),
        SCREENSHOT_TOOL_PANEL_CSS.removeprefix("\n"),
        SCREENSHOT_EDITOR_CSS.removeprefix("\n"),
        SCREENSHOT_RESPONSIVE_CSS.removeprefix("\n"),
    ]
)
