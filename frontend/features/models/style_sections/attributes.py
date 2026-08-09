MODELS_ATTRIBUTES_CSS = """
    /*
     * Attribute cards
     */

    [class*="st-key-model_attribute_summary_"] {
        overflow: visible;

        margin-top: 0.25rem;
        margin-bottom: 0.95rem;
        padding: 0.75rem 0.8rem 1.05rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface-muted);
    }

    [class*="st-key-model_attribute_summary_"] [data-testid="column"]:last-child {
        display: flex;
        justify-content: flex-end;

        padding-right: 0;
    }

    [class*="st-key-model_attribute_summary_"] > div > div > [data-testid="column"]:last-child [data-testid="stButton"] {
        display: flex;
        justify-content: flex-end;

        width: 100%;
    }

    [class*="st-key-model_attribute_summary_"] [data-testid="stButton"] button {
        min-width: 8.2rem;
        white-space: nowrap;
    }

    [class*="st-key-model_attribute_summary_"]
    [data-testid="stDataFrame"] {
        overflow: hidden;

        border: 1px solid var(--cogsim-border);
        border-radius: 10px;

        background: var(--cogsim-surface);
    }

    .cogsim-attribute-value-grid-spacer {
        padding-bottom: 0.35rem;
    }

    [class*="st-key-attribute_value_card_"] {
        min-height: 98px;
        margin-bottom: 0.64rem;
        padding: 0.74rem 0.82rem 0.68rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(250, 250, 255, 0.92)),
            var(--cogsim-surface);
        box-shadow: 0 8px 22px rgba(17, 24, 39, 0.025);
    }

    .cogsim-attribute-value-card__content {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.85rem;
    }

    .cogsim-attribute-value-card__label {
        color: var(--cogsim-primary);
        font-size: 0.75rem;
        font-weight: 760;
        line-height: 1.25;
    }

    .cogsim-attribute-value-card__description {
        max-width: 88%;
        margin-top: 0.2rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.66rem;
        font-weight: 450;
        line-height: 1.34;
    }

    .cogsim-attribute-value-card__value {
        flex: 0 0 auto;

        min-width: 2.4rem;
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

    .cogsim-attribute-value-card__scale {
        margin-top: 0.62rem;
    }

    .cogsim-attribute-value-card__track {
        height: 0.42rem;

        overflow: hidden;

        border-radius: 999px;

        background: rgba(226, 232, 240, 0.9);
    }

    .cogsim-attribute-value-card__track span {
        display: block;
        height: 100%;
        min-width: 0.25rem;

        border-radius: inherit;

        background: linear-gradient(90deg, var(--cogsim-primary), #8b7cf6);
    }

    .cogsim-attribute-value-card__scale-labels {
        display: flex;
        justify-content: space-between;

        margin-top: 0.28rem;

        color: var(--cogsim-text-muted);
        font-size: 0.58rem;
        font-weight: 650;
        line-height: 1.2;
    }

    .cogsim-attribute-info-placeholder {
        display: inline-flex;
        width: 1.35rem;
        height: 1.35rem;
    }

"""
