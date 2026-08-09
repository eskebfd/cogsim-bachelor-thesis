RESULT_COMPARISON_PROFILE_CARDS_CSS = """
    .cogsim-profile-comparison-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.82rem;
    }

    .cogsim-profile-comparison-card {
        min-height: 154px;
        padding: 0.9rem;

        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 18px;

        background: rgba(255, 255, 255, 0.9);
    }

    .cogsim-profile-comparison-card__title {
        color: var(--cogsim-text);
        font-size: 0.84rem;
        font-weight: 760;
        line-height: 1.25;
    }

    .cogsim-profile-comparison-card__subtitle {
        min-height: 2.1rem;
        margin-top: 0.24rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        line-height: 1.4;
    }

    .cogsim-profile-comparison-card__rows {
        display: grid;
        gap: 0.44rem;
        margin-top: 0.75rem;
    }

    .cogsim-profile-score-row {
        display: grid;
        grid-template-columns: 4.2rem 1fr 2.8rem;
        align-items: center;
        gap: 0.48rem;
    }

    .cogsim-profile-score-row__label {
        overflow: hidden;

        color: var(--cogsim-text-secondary);
        font-size: 0.68rem;
        font-weight: 650;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .cogsim-profile-score-row__track {
        height: 0.28rem;
        overflow: hidden;

        border-radius: 999px;

        background: #E8EAF2;
    }

    .cogsim-profile-score-row__bar {
        display: block;
        height: 100%;
        border-radius: inherit;
    }

    .cogsim-profile-score-row__value {
        color: var(--cogsim-text);
        font-size: 0.68rem;
        font-weight: 760;
        text-align: right;
        white-space: nowrap;
    }

    /*
    - Profile detail KPI cards
     */

    .cogsim-profile-kpi-grid {
        display: grid;
        grid-template-columns: repeat(6, minmax(0, 1fr));
        gap: 0.65rem;

        margin: 0.15rem 0 1rem;
    }

    .cogsim-profile-kpi-card {
        position: relative;
        min-height: 92px;
        overflow: hidden;

        padding: 0.72rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 15px;

        background: rgba(255, 255, 255, 0.86);
    }

    .cogsim-profile-kpi-card__label {
        color: var(--cogsim-text-secondary);
        font-size: 0.66rem;
        font-weight: 760;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .cogsim-profile-kpi-card__value {
        margin-top: 0.35rem;

        color: var(--cogsim-text);
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    .cogsim-profile-kpi-card__detail {
        margin-top: 0.3rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.68rem;
        line-height: 1.3;
    }

    .cogsim-profile-kpi-card__spark {
        position: absolute;
        right: 0.62rem;
        bottom: 0.62rem;

        width: 1.8rem;
        height: 1.8rem;

        border-radius: 999px;

        background:
            radial-gradient(circle at center, #ffffff 54%, transparent 57%),
            conic-gradient(var(--cogsim-primary) var(--score), #EEF2FF 0deg);
        opacity: 0.9;
    }

    .cogsim-profile-kpi-card--success .cogsim-profile-kpi-card__spark {
        background:
            radial-gradient(circle at center, #ffffff 54%, transparent 57%),
            conic-gradient(var(--cogsim-success) var(--score), #EEF2FF 0deg);
    }

    .cogsim-profile-kpi-card--warning .cogsim-profile-kpi-card__spark {
        background:
            radial-gradient(circle at center, #ffffff 54%, transparent 57%),
            conic-gradient(var(--cogsim-warning) var(--score), #EEF2FF 0deg);
    }

    .cogsim-profile-kpi-card--danger .cogsim-profile-kpi-card__spark {
        background:
            radial-gradient(circle at center, #ffffff 54%, transparent 57%),
            conic-gradient(var(--cogsim-danger) var(--score), #EEF2FF 0deg);
    }
"""
