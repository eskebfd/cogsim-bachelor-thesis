MODELS_RESPONSIVE_CSS = """
    /*
     * Expanders
     */

    [class*="st-key-models_review"]
    [data-testid="stExpander"] {
        margin-top: 0.6rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 10px;

        background: var(--cogsim-surface);
    }

    [class*="st-key-models_review"]
    [data-testid="stExpander"] summary {
        min-height: 38px;
        padding: 0.45rem 0.65rem;

        color: var(--cogsim-text);
        font-size: 0.72rem;
        font-weight: 600;
    }

    @media (max-width: 900px) {
        .cogsim-attribute-value-grid,
        .cogsim-hta-step__meta-grid,
        .cogsim-user-comparison-grid {
            grid-template-columns: 1fr;
        }

        .cogsim-hta-step__topline {
            flex-direction: column;
            gap: 0.35rem;
        }
    }

"""
