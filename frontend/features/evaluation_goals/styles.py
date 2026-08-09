EVALUATION_GOALS_CSS = """
    /*
     * Intro
     */

    .cogsim-evaluation-intro {
        margin-bottom: 0.9rem;
        padding: 0.85rem 1rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface);
    }

    .cogsim-evaluation-intro__title {
        margin-bottom: 0.2rem;

        color: var(--cogsim-text);
        font-size: 0.86rem;
        font-weight: 650;
        line-height: 1.35;
    }

    .cogsim-evaluation-intro__text {
        color: var(--cogsim-text-secondary);
        font-size: 0.76rem;
        line-height: 1.4;
    }

    /*
     * Evaluation goal cards
     */

    [class*="st-key-evaluation_goal_card_"],
    [class*="st-key-evaluation_metric_card_"] {
        position: relative;

        min-height: 0;
        height: auto;

        margin-bottom: 0.65rem;
        padding: 0.95rem;

        overflow: visible;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface);

        transition:
            border-color 0.15s ease,
            box-shadow 0.15s ease,
            background-color 0.15s ease;
    }

    [class*="st-key-evaluation_goal_card_"]:hover,
    [class*="st-key-evaluation_metric_card_"]:hover {
        border-color: var(--cogsim-border-strong);
        box-shadow: var(--cogsim-shadow);
    }

    [class*="st-key-evaluation_metric_card_"]:has(input:checked) {
        border-color: rgba(124, 77, 255, 0.52);
        background: var(--cogsim-primary-soft);
    }

    /*
     * Card content
     */

    .cogsim-evaluation-card-header {
        display: flex;
        align-items: flex-start;
        gap: 0.68rem;
    }

    .cogsim-evaluation-card-icon {
        display: flex;
        width: 36px;
        height: 36px;
        flex: 0 0 36px;
        align-items: center;
        justify-content: center;

        border: 1px solid var(--cogsim-border);
        border-radius: 10px;

        background: var(--cogsim-surface-muted);
        color: var(--cogsim-primary);
    }

    .cogsim-evaluation-card-icon .cogsim-icon,
    .cogsim-evaluation-card-icon svg {
        display: block;
        color: inherit;
        stroke: currentColor;
    }

    .cogsim-evaluation-card-copy {
        min-width: 0;
        padding-right: 0;
    }

    .cogsim-evaluation-card-title {
        margin-bottom: 0.22rem;

        color: var(--cogsim-text);
        font-size: 0.86rem;
        font-weight: 650;
        line-height: 1.35;
    }

    .cogsim-evaluation-card-description {
        margin-bottom: 0.54rem;

        color: var(--cogsim-text);
        font-size: 0.79rem;
        font-weight: 500;
        line-height: 1.42;

        overflow-wrap: break-word;
    }

    .cogsim-evaluation-card-example {
        display: grid;
        grid-template-columns: minmax(72px, auto) 1fr;
        gap: 0.5rem;

        margin-top: 0.5rem;
        padding: 0.58rem 0.65rem;

        border: 1px solid rgba(124, 77, 255, 0.12);
        border-radius: 10px;

        background: rgba(124, 77, 255, 0.045);
        color: var(--cogsim-text-secondary);
        font-size: 0.75rem;
        line-height: 1.38;
    }

    .cogsim-evaluation-card-example span {
        color: var(--cogsim-primary);
        font-weight: 650;
    }

    /*
     * Selection checkbox
     */

    [class*="st-key-evaluation_metric_card_"] [data-testid="stCheckbox"] {
        margin-top: 0.72rem;
    }

    [class*="st-key-evaluation_metric_card_"] [data-testid="stCheckbox"] label {
        display: inline-flex;
        width: auto;
        min-height: 24px;
        align-items: center;
        gap: 0.35rem;

        padding: 0;

        color: var(--cogsim-text-secondary);
    }

    [class*="st-key-evaluation_metric_card_"]
    [data-testid="stCheckbox"] label p {
        color: inherit;
        font-size: 0.7rem;
        font-weight: 650;
        line-height: 1.2;
    }

    [class*="st-key-evaluation_metric_card_"]:has(input:checked)
    [data-testid="stCheckbox"] label {
        color: var(--cogsim-primary);
    }

    /*
     * Responsive layout
     */

    @media (max-width: 900px) {
        [class*="st-key-evaluation_goal_card_"],
        [class*="st-key-evaluation_metric_card_"] {
            height: auto;
            min-height: 0;
        }

        .cogsim-evaluation-card-icon {
            width: 34px;
            height: 34px;
            flex-basis: 34px;
        }
    }

    @media (max-width: 700px) {
        [class*="st-key-evaluation_goal_card_"],
        [class*="st-key-evaluation_metric_card_"] {
            padding: 0.85rem;
        }

        .cogsim-evaluation-card-header {
            gap: 0.6rem;
        }

        .cogsim-evaluation-card-title {
            font-size: 0.8rem;
        }

        .cogsim-evaluation-card-description {
            font-size: 0.76rem;
        }

        .cogsim-evaluation-card-example {
            grid-template-columns: 1fr;
            gap: 0.1rem;
        }
    }
"""
