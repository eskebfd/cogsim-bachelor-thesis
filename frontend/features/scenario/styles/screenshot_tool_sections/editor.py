SCREENSHOT_EDITOR_CSS = """
    /*
     * Step descriptions
     */

    [class*="st-key-screenshot_analysis_result"]
    [data-testid="stCaptionContainer"] {
        margin: 0.1rem 0 0.2rem 0.5rem;
    }

    [class*="st-key-screenshot_analysis_result"]
    [data-testid="stCaptionContainer"] p {
        margin: 0;

        color: var(--cogsim-text-secondary);
        font-size: 0.7rem;
        line-height: 1.3;
    }

    /*
     * Compact expander
     */

    [class*="st-key-screenshot_analysis_result"]
    [data-testid="stExpander"] {
        margin-top: 0.45rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 9px;

        background: var(--cogsim-surface-muted);
    }

    [class*="st-key-screenshot_analysis_result"]
    [data-testid="stExpander"] summary {
        min-height: 36px;
        padding: 0.45rem 0.6rem;

        color: var(--cogsim-text);
        font-size: 0.74rem;
        font-weight: 600;
    }

    [class*="st-key-screenshot_analysis_result"]
    [data-testid="stExpanderDetails"] {
        padding: 0 0.65rem 0.6rem;
    }

    [class*="st-key-screenshot_analysis_result"]
    [data-testid="stExpanderDetails"] p,
    [class*="st-key-screenshot_analysis_result"]
    [data-testid="stExpanderDetails"] li {
        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        line-height: 1.35;
    }

"""
