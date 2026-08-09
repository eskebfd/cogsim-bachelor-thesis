CARDS_CSS = """
    .cogsim-card {
        background: var(--cogsim-surface);
        border: 1px solid var(--cogsim-border);
        border-radius: var(--cogsim-radius);
        padding: 1rem;
        box-shadow: var(--cogsim-shadow);
    }

    .cogsim-soft-card {
        background: var(--cogsim-surface-muted);
        border: 1px solid var(--cogsim-border);
        border-radius: 14px;
        padding: 0.8rem 0.9rem;
    }

    .cogsim-card-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin: 0 0 0.35rem;
        color: var(--cogsim-text);
        font-size: 1rem;
        font-weight: 700;
    }

    .cogsim-card-description {
        margin: 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .cogsim-kpi-card {
        min-height: 116px;
        padding: 0.9rem;
        background: var(--cogsim-surface);
        border: 1px solid var(--cogsim-border);
        border-radius: 14px;
        box-shadow: var(--cogsim-shadow);

        display: flex;
        flex-direction: column;
    }

    .cogsim-kpi-label {
        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    .cogsim-kpi-value {
        margin-top: 0.35rem;
        color: var(--cogsim-text);
        font-weight: 730;
        line-height: 1.2;

        overflow-wrap: anywhere;
        white-space: normal;
    }

    .cogsim-kpi-value--numeric {
        font-size: 1.35rem;
    }

    .cogsim-kpi-value--text {
        font-size: 0.92rem;
        font-weight: 700;
        line-height: 1.3;
        letter-spacing: -0.01em;
        hyphens: auto;
    }

    .cogsim-kpi-caption {
        margin-top: 0.25rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.84rem;
        line-height: 1.35;
    }

    @media (max-width: 900px) {
        .cogsim-kpi-card {
            min-height: 104px;
        }

        .cogsim-kpi-value--numeric {
            font-size: 1.22rem;
        }

        .cogsim-kpi-value--text {
            font-size: 0.86rem;
        }
    }
"""
