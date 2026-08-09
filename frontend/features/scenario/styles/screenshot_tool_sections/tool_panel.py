SCREENSHOT_TOOL_PANEL_CSS = """
    /*
     * Compact screenshot analysis
     */

    [class*="st-key-screenshot_analysis_result"] {
        max-width: 860px;
        margin: 0.7rem auto 0;
        padding: 1rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 16px;

        background: var(--cogsim-surface);
    }

    .cogsim-screenshot-analysis__header {
        margin-bottom: 0.85rem;
    }

    .cogsim-screenshot-analysis__eyebrow {
        display: inline-flex;
        align-items: center;

        margin-bottom: 0.35rem;
        padding: 0.2rem 0.48rem;

        border: 1px solid rgba(22, 138, 74, 0.22);
        border-radius: 999px;

        background: rgba(22, 138, 74, 0.07);
        color: var(--cogsim-success);

        font-size: 0.62rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        line-height: 1.2;
        text-transform: uppercase;
    }

    .cogsim-screenshot-analysis__title {
        color: var(--cogsim-text);
        font-size: 1rem;
        font-weight: 720;
        line-height: 1.25;
    }

    .cogsim-screenshot-analysis__copy {
        max-width: 620px;
        margin-top: 0.25rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.76rem;
        line-height: 1.45;
    }

    .cogsim-screenshot-summary-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.65rem;

        margin-bottom: 0.9rem;
    }

    .cogsim-screenshot-summary-card {
        padding: 0.7rem 0.75rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface-muted);
    }

    .cogsim-screenshot-summary-card__label {
        margin-bottom: 0.28rem;

        color: var(--cogsim-text-muted);
        font-size: 0.62rem;
        font-weight: 750;
        letter-spacing: 0.06em;
        line-height: 1.2;
        text-transform: uppercase;
    }

    .cogsim-screenshot-summary-card__value {
        color: var(--cogsim-text);
        font-size: 0.84rem;
        font-weight: 650;
        line-height: 1.35;
    }

    .cogsim-screenshot-analysis__section-title {
        margin-bottom: 0.45rem;

        color: var(--cogsim-text);
        font-size: 0.82rem;
        font-weight: 720;
        line-height: 1.3;
    }

    [class*="st-key-screenshot_analysis_result"] h4 {
        margin: 0 0 0.45rem;

        color: var(--cogsim-text);
        font-size: 0.9rem;
        font-weight: 650;
        line-height: 1.3;
    }

    [class*="st-key-screenshot_analysis_result"] p {
        margin-top: 0.1rem;
        margin-bottom: 0.25rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        line-height: 1.35;
    }

    [class*="st-key-screenshot_analysis_result"] strong {
        color: var(--cogsim-text);
        font-weight: 650;
    }

    /*
     * Compact HTA steps
     */

    .cogsim-hta-step {
        display: flex;
        align-items: center;
        gap: 0.55rem;

        margin-top: 0.35rem;
        padding: 0.5rem 0.65rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 11px;

        background: var(--cogsim-surface-muted);
    }

    .cogsim-hta-step__number {
        display: inline-flex;
        width: 1.45rem;
        height: 1.45rem;
        flex: 0 0 1.45rem;
        align-items: center;
        justify-content: center;

        border-radius: 999px;

        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);

        font-size: 0.68rem;
        font-weight: 750;
        line-height: 1;
    }

    .cogsim-hta-step__title {
        display: block;

        color: var(--cogsim-text);
        font-size: 0.78rem;
        font-weight: 650;
        line-height: 1.3;
    }

"""
