RESULT_COMPARISON_CORE_CSS = """
    /*
    - Profile comparison report
     */

    .cogsim-profile-comparison-panel {
        margin: 0 0 1.1rem;
        padding: 1.05rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 22px;

        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.99), rgba(250, 250, 255, 0.94)),
            var(--cogsim-surface);
        box-shadow: 0 18px 45px rgba(38, 35, 80, 0.06);
    }

    [class*="st-key-result_navigation_tabs"] {
        margin-bottom: 1.05rem;
        padding: 0.28rem;
        border: 1px solid var(--cogsim-border);
        border-radius: 13px;
        background: rgba(255, 255, 255, 0.74);
    }

    [class*="st-key-result_navigation_tabs"] [data-testid="stRadio"] > div {
        gap: 0.3rem;
    }

    [class*="st-key-result_navigation_tabs"] label {
        min-height: 2.25rem;
        padding: 0.42rem 0.75rem;
        border: 1px solid transparent;
        border-radius: 10px;
        color: var(--cogsim-text-secondary);
        font-size: 0.82rem;
        font-weight: 680;
        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            color 0.15s ease;
    }

    [class*="st-key-result_navigation_tabs"] input[type="radio"],
    [class*="st-key-result_navigation_tabs"] [data-baseweb="radio"] > div:first-child {
        display: none;
    }

    [class*="st-key-result_navigation_tabs"] label:has(input:checked) {
        border-color: rgba(109, 93, 251, 0.18);
        background: rgba(245, 243, 255, 0.92);
        color: var(--cogsim-primary);
        box-shadow: 0 1px 4px rgba(109, 93, 251, 0.08);
    }

    .cogsim-result-section-heading {
        display: block;
        margin-bottom: 0.85rem;
    }

    .cogsim-result-section-heading span {
        color: var(--cogsim-text);
        font-size: 1rem;
        font-weight: 760;
        letter-spacing: -0.02em;
    }

    .cogsim-result-section-heading small {
        display: block;
        margin-top: 0.15rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        font-weight: 560;
        line-height: 1.4;
    }

    .cogsim-result-section-copy {
        margin: 0.25rem 0 0.85rem;
    }

    .cogsim-result-section-copy h4 {
        margin: 0 0 0.25rem;
        color: var(--cogsim-text);
        font-size: 1.05rem;
        font-weight: 790;
        letter-spacing: -0.02em;
    }

    .cogsim-result-section-copy p {
        max-width: 62rem;
        margin: 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.86rem;
        line-height: 1.48;
    }

    [class*="st-key-result_interpretation_hub"] {
        margin: 0.35rem 0 1.2rem;
        padding: 0;

        border: 0;
        background: transparent;
        box-shadow: none;
    }

    [class*="st-key-result_interpretation_hub"] .cogsim-result-section-heading {
        margin-bottom: 0.45rem;
        padding-bottom: 0.65rem;
        border-bottom: 1px solid rgba(109, 93, 251, 0.12);
    }

    [class*="st-key-result_interpretation_hub"] .cogsim-result-section-heading span {
        font-size: 1.08rem;
    }

    [class*="st-key-result_interpretation_hub"] .cogsim-explain-grid,
    [class*="st-key-result_interpretation_hub"] .cogsim-result-legend-grid {
        grid-template-columns: 1fr;
    }

    [class*="st-key-result_interpretation_hub"] .cogsim-explain-card {
        box-shadow: none;
    }

    [class*="st-key-result_interpretation_hub"] [data-testid="stExpander"] {
        border-color: rgba(109, 93, 251, 0.16);
        border-radius: 16px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.72);
    }

"""
