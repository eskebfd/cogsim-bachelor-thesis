COMPUTED_PARAMETERS_CSS = """
    [class*="st-key-simulation_plan_review"] {
        padding: 0;
    }

    .cogsim-plan-intro {
        margin-bottom: 0.9rem;
        padding: 0.72rem 0.82rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface-muted);
    }

    .cogsim-plan-intro__hint {
        display: inline-flex;
        align-items: center;

        padding: 0.42rem 0.62rem;

        border: 1px solid rgba(220, 38, 38, 0.22);
        border-radius: 999px;

        background: rgba(220, 38, 38, 0.08);
        color: var(--cogsim-danger);

        font-size: 0.72rem;
        font-weight: 650;
        line-height: 1.35;
    }

    .cogsim-plan-section-title {
        margin: 0.95rem 0 0.5rem;

        color: var(--cogsim-text);
        font-size: 0.8rem;
        font-weight: 650;
        line-height: 1.35;
    }

    .cogsim-plan-value-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.62rem;

        margin-bottom: 0.8rem;
    }

    .cogsim-plan-value-card {
        padding: 0.68rem 0.72rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface-muted);
    }

    .cogsim-plan-value-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .cogsim-plan-value-card__label {
        color: var(--cogsim-text);
        font-size: 0.72rem;
        font-weight: 600;
        line-height: 1.3;
    }

    .cogsim-plan-value-card__value {
        flex: 0 0 auto;

        padding: 0.18rem 0.45rem;

        border: 1px solid rgba(124, 77, 255, 0.18);
        border-radius: 999px;

        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);

        font-size: 0.72rem;
        font-weight: 750;
        line-height: 1.2;
        text-align: center;
    }

    [class*="st-key-simulation_plan_review"]
    [data-testid="stDataFrame"] {
        margin-bottom: 0.8rem;

        overflow: hidden;

        border: 1px solid var(--cogsim-border);
        border-radius: 10px;

        background: var(--cogsim-surface);
    }

    @media (max-width: 900px) {
        .cogsim-plan-value-grid {
            grid-template-columns: 1fr;
        }
    }
"""
