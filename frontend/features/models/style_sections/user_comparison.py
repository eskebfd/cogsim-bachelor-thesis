MODELS_USER_COMPARISON_CSS = """
    /*
     * User comparison
     */

    .cogsim-user-comparison-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.68rem;

        margin-bottom: 0.95rem;
    }

    .cogsim-user-comparison-card {
        display: flex;
        flex-direction: column;
        gap: 0.58rem;

        padding: 0.78rem 0.82rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(250, 250, 255, 0.9)),
            var(--cogsim-surface);
    }

    .cogsim-user-comparison-card__attribute {
        color: var(--cogsim-text);
        color: var(--cogsim-primary);
        font-size: 0.76rem;
        font-weight: 700;
        line-height: 1.35;
    }

    .cogsim-user-comparison-card__description,
    p.cogsim-user-comparison-card__description {
        margin: -0.3rem 0 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.6rem !important;
        font-weight: 460;
        line-height: 1.28 !important;
    }

    .cogsim-user-comparison-card__values {
        display: grid;
        gap: 0.4rem;
    }

    .cogsim-user-comparison-value-row {
        display: grid;
        grid-template-columns: minmax(7rem, 0.9fr) minmax(0, 1.1fr);
        align-items: center;
        gap: 0.5rem;
    }

    .cogsim-user-comparison-value-row__label {
        display: flex;
        justify-content: space-between;
        gap: 0.45rem;
        min-width: 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.68rem;
        font-weight: 650;
        line-height: 1.2;
    }

    .cogsim-user-comparison-value-row__label strong {
        color: var(--cogsim-primary);
        font-size: 0.67rem;
        font-weight: 780;
    }

    .cogsim-user-comparison-value-row__track {
        height: 0.42rem;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(226, 232, 240, 0.88);
    }

    .cogsim-user-comparison-value-row__track span {
        display: block;
        height: 100%;
        min-width: 0.25rem;
        border-radius: inherit;
    }

"""
