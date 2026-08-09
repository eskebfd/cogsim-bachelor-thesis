MODELS_USER_PROFILES_CSS = """
    /*
     * Task structure
     */

    [class*="st-key-task_structure_review"] {
        margin-top: 0.25rem;
        margin-bottom: 0.75rem;
        padding: 0.8rem 0.8rem 0.95rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface-muted);
    }

    .cogsim-hta-timeline {
        position: relative;

        display: flex;
        flex-direction: column;
        gap: 0.52rem;

        margin-bottom: 1.05rem;
        padding-left: 0.12rem;
    }

    [class*="st-key-missing_task_step"] {
        margin-top: 1.1rem;
    }

    [class*="st-key-task_step_edit_form_"] {
        margin: 0.18rem 0 0.72rem;
        width: 100%;
        box-sizing: border-box;
        padding: 0.62rem 0.68rem;
        border: 1px solid var(--cogsim-border);
        border-radius: 12px;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(250, 250, 255, 0.92)),
            var(--cogsim-surface);
    }

    [class*="st-key-task_structure_review"] [data-testid="stExpander"],
    [data-testid="stExpander"]:has([class*="st-key-task_step_edit_form_"]) {
        margin: 0.18rem 0 0.72rem;
        width: 100%;
        box-sizing: border-box;
        border: 1px solid var(--cogsim-border);
        border-radius: 12px;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(250, 250, 255, 0.92)),
            var(--cogsim-surface);
        box-shadow: 0 8px 22px rgba(17, 24, 39, 0.035);
    }

    [class*="st-key-task_structure_review"] [data-testid="stExpander"] summary,
    [data-testid="stExpander"]:has([class*="st-key-task_step_edit_form_"]) summary {
        min-height: 30px !important;
        padding: 0.3rem 0.5rem !important;
        color: var(--cogsim-text-secondary);
        font-size: 0.64rem !important;
        font-weight: 700;
    }

    [class*="st-key-task_structure_review"] [data-testid="stExpander"] summary p,
    [data-testid="stExpander"]:has([class*="st-key-task_step_edit_form_"]) summary p,
    [data-testid="stExpander"]:has([class*="st-key-task_step_edit_form_"]) [data-testid="stMarkdownContainer"] p,
    [data-testid="stExpander"]:has([class*="st-key-task_step_edit_form_"]) label,
    [data-testid="stExpander"]:has([class*="st-key-task_step_edit_form_"]) input,
    [data-testid="stExpander"]:has([class*="st-key-task_step_edit_form_"]) textarea {
        font-size: 0.66rem !important;
        line-height: 1.35;
    }

    [class*="st-key-missing_task_step"] [data-testid="stTextInput"] input {
        font-size: 0.72rem;
    }

    .cogsim-hta-timeline::before {
        content: "";
        position: absolute;
        top: 1rem;
        bottom: 1rem;
        left: 1.12rem;

        width: 1px;

        background: rgba(124, 77, 255, 0.22);
    }

    .cogsim-hta-step {
        position: relative;

        display: grid;
        grid-template-columns: auto minmax(0, 1fr);
        gap: 0.7rem;
        align-items: flex-start;

        padding: 0.72rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface);
        box-shadow: 0 8px 22px rgba(17, 24, 39, 0.035);
    }

    .cogsim-hta-step__marker {
        display: flex;
        align-items: center;
        justify-content: center;

        width: 2rem;
        height: 2rem;

        border: 1px solid rgba(124, 77, 255, 0.18);
        border-radius: 999px;

        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);

        font-size: 0.72rem;
        font-weight: 750;
        z-index: 1;
    }

    .cogsim-hta-step__content {
        min-width: 0;
    }

    .cogsim-hta-step__topline {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.75rem;

        margin-bottom: 0.22rem;
    }

    .cogsim-hta-step__title {
        color: var(--cogsim-text);
        font-size: 0.8rem;
        font-weight: 700;
        line-height: 1.35;
    }

    .cogsim-hta-step__duration {
        flex: 0 0 auto;

        padding: 0.18rem 0.5rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 999px;

        background: var(--cogsim-surface-muted);
        color: var(--cogsim-text-secondary);

        font-size: 0.67rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .cogsim-hta-step__description {
        margin-bottom: 0.58rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        line-height: 1.45;
    }

    .cogsim-hta-step__meta-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.5rem;
    }

    .cogsim-hta-step__meta {
        padding: 0.5rem 0.55rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 9px;

        background: var(--cogsim-surface-muted);
    }

    .cogsim-hta-step__meta-label {
        display: block;
        margin-bottom: 0.16rem;

        color: var(--cogsim-text-muted);
        font-size: 0.6rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .cogsim-hta-step__meta-value {
        display: block;

        color: var(--cogsim-text-secondary);
        font-size: 0.68rem;
        line-height: 1.4;
    }

"""
