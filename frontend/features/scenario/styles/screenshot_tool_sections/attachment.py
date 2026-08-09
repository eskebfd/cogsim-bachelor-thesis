SCREENSHOT_ATTACHMENT_CSS = """
    /*
     * Task attachment callout
     */

    [class*="st-key-scenario_task_screenshot_attachment"] {
        margin: -0.15rem 0 0.85rem;
        padding: 0.42rem 0.5rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: rgba(248, 247, 255, 0.22);
    }

    .cogsim-task-screenshot-callout {
        display: flex;
        align-items: center;
        gap: 0.5rem;

        margin-bottom: 0.28rem;
    }

    .cogsim-task-screenshot-callout__icon {
        display: inline-flex;
        width: 24px;
        height: 24px;
        flex: 0 0 24px;
        align-items: center;
        justify-content: center;

        border: 1px solid rgba(91, 91, 214, 0.2);
        border-radius: 9px;

        background: var(--cogsim-surface);
        color: var(--cogsim-primary);
    }

    .cogsim-task-screenshot-callout__title {
        color: var(--cogsim-text);
        font-size: 0.7rem;
        font-weight: 700;
        line-height: 1.3;
    }

    .cogsim-task-screenshot-callout__text {
        max-width: 760px;
        margin-top: 0.18rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.64rem;
        line-height: 1.42;
    }

"""
