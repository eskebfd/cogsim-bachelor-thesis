from frontend.features.scenario.styles.scenario_form import SCENARIO_FORM_CSS
from frontend.features.scenario.styles.screenshot_tool import SCREENSHOT_TOOL_CSS


SCENARIO_COMMON_CSS = """
    /*
     * Scenario input layout
     */

    [class*="st-key-scenario_text_panel"] {
        height: 100%;
        padding: 1.25rem;

        background: var(--cogsim-surface);
        border: 1px solid var(--cogsim-border);
        border-radius: 16px;

        box-shadow: var(--cogsim-shadow);
    }

    /*
     * Section header
     */

    .cogsim-scenario-section-header {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;

        margin-bottom: 0.85rem;
        padding: 0.78rem 0.85rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 13px;

        background: var(--cogsim-surface-muted);
    }

    .cogsim-scenario-section-icon {
        display: flex;
        width: 38px;
        height: 38px;
        flex: 0 0 38px;
        align-items: center;
        justify-content: center;

        border: 1px solid var(--cogsim-border);
        border-radius: 10px;

        background: var(--cogsim-surface-muted);
        color: var(--cogsim-primary);
    }

    .cogsim-scenario-section-icon .cogsim-icon,
    .cogsim-scenario-section-icon svg {
        display: block;
        color: inherit;
        stroke: currentColor;
    }

    .cogsim-scenario-section-title {
        color: var(--cogsim-text);
        font-size: 0.95rem;
        font-weight: 650;
        line-height: 1.3;
    }

    .cogsim-scenario-section-description {
        margin-top: 0.2rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.8rem;
        line-height: 1.45;
    }

    /*
     * Scenario field heading
     */

    .cogsim-scenario-field-heading {
        display: flex;
        align-items: center;
        gap: 0.62rem;

        margin: 1.05rem 0 0.48rem;
    }

    .cogsim-scenario-field-heading__icon {
        display: inline-flex;
        width: 32px;
        height: 32px;
        flex: 0 0 32px;
        align-items: center;
        justify-content: center;

        border: 1px solid rgba(124, 77, 255, 0.18);
        border-radius: 10px;

        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);
    }

    .cogsim-scenario-field-heading__title {
        color: var(--cogsim-text);
        font-size: 0.95rem;
        font-weight: 720;
        line-height: 1.25;
    }

    .cogsim-scenario-field-heading__description {
        margin-top: 0.1rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.76rem;
        line-height: 1.35;
    }

    /*
     * Responsive layout
     */

    @media (max-width: 900px) {
        [class*="st-key-scenario_text_panel"] {
            padding: 1rem;
        }
    }
"""


SCENARIO_CSS = "\n".join(
    [
        SCENARIO_COMMON_CSS,
        SCENARIO_FORM_CSS,
        SCREENSHOT_TOOL_CSS,
    ]
)
