MODELS_REVIEW_CARDS_CSS = """
    /*
     * Tabs
     */

    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.35rem;

        margin-bottom: 0.75rem;
        padding: 0.25rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 10px;

        background: var(--cogsim-surface-muted);
    }

    [data-testid="stTabs"] [data-baseweb="tab"] {
        min-height: 34px;

        padding: 0.4rem 0.75rem;

        border: 1px solid transparent;
        border-radius: 8px;

        background: transparent;
        color: var(--cogsim-text-secondary);

        font-size: 0.74rem;
        font-weight: 600;
        letter-spacing: 0.04em;

        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            color 0.15s ease,
            box-shadow 0.15s ease;
    }

    [data-testid="stTabs"] [data-baseweb="tab"]:hover {
        background: rgba(124, 77, 255, 0.05);
        color: var(--cogsim-text);
    }

    [data-testid="stTabs"] [aria-selected="true"] {
        background: var(--cogsim-primary-soft);
        border-color: rgba(124, 77, 255, 0.18);

        color: var(--cogsim-primary);
        font-weight: 700;

        box-shadow: 0 1px 3px rgba(124, 77, 255, 0.08);
    }

    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        display: none;
    }

    [data-testid="stTabs"] [data-baseweb="tab-border"] {
        display: none;
    }

    [class*="st-key-models_review_tab_selector"] [role="radiogroup"] {
        display: flex;
        gap: 0.35rem;

        margin-bottom: 0.75rem;
        padding: 0.25rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 10px;

        background: var(--cogsim-surface-muted);
    }

    [class*="st-key-models_review_tab_selector"] label {
        flex: 0 0 auto;

        min-height: 34px;
        padding: 0.4rem 0.75rem;

        border: 1px solid transparent;
        border-radius: 8px;

        color: var(--cogsim-text-secondary);
        font-size: 0.74rem;
        font-weight: 600;
        letter-spacing: 0.04em;

        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            color 0.15s ease,
            box-shadow 0.15s ease;
    }

    [class*="st-key-models_review_tab_selector"] label:hover {
        background: rgba(124, 77, 255, 0.05);
        color: var(--cogsim-text);
    }

    [class*="st-key-models_review_tab_selector"] label:has(input:checked) {
        background: var(--cogsim-primary-soft);
        border-color: rgba(124, 77, 255, 0.18);

        color: var(--cogsim-primary);
        font-weight: 700;

        box-shadow: 0 1px 3px rgba(124, 77, 255, 0.08);
    }

    [class*="st-key-models_review_tab_selector"] label > div:first-child {
        display: none;
    }

"""
