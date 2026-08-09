TIMELINE_CSS = """
    /*
     * Horizontal workflow timeline
     */

    .st-key-workflow_stepper_v7 {
        width: 100%;
        margin: 0.25rem 0 1.5rem;
    }

    .cogsim-workflow-timeline {
        position: relative;
        display: flex;
        align-items: flex-start;
        overflow-x: auto;
        gap: 0;
        padding: 0.4rem 0.25rem 0.2rem;
    }

    /*
     * Connecting timeline line
     */
    .cogsim-workflow-timeline::before {
        content: "";
        position: absolute;
        top: 1.35rem;
        left: 6.25%;
        right: 6.25%;
        height: 2px;
        background: var(--cogsim-border-strong);
        z-index: 0;
    }

    .cogsim-workflow-timeline > .cogsim-timeline-step {
        position: relative;
        z-index: 1;
        flex: 1 0 104px;
        min-width: 104px;
        text-align: center;
    }

    .cogsim-timeline-step {
        display: flex;
        width: 100%;
        flex-direction: column;
        align-items: center;
    }

    /*
     * Round timeline circle
     */
    .cogsim-timeline-point {
        display: flex;
        width: 32px;
        height: 32px;
        min-width: 32px;
        min-height: 32px;
        align-items: center;
        justify-content: center;

        border: 2px solid var(--cogsim-border-strong);
        border-radius: 50%;

        background: var(--cogsim-surface);
        color: var(--cogsim-text-muted);

        font-size: 0.75rem;
        font-weight: 600;
        line-height: 1;

        box-shadow: 0 0 0 6px var(--cogsim-background);
    }

    /*
     * Step label always shown underneath the number
     */
    .cogsim-timeline-label {
        max-width: 8rem;
        margin-top: 0.6rem;

        color: var(--cogsim-text-muted);

        font-size: 0.68rem;
        font-weight: 500;
        line-height: 1.25;
        text-align: center;
        white-space: normal;
    }

    /*
     * Completed steps
     */
    .cogsim-timeline-step.is-completed
    .cogsim-timeline-point {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-surface);
        color: var(--cogsim-primary);
    }

    .cogsim-timeline-step.is-completed
    .cogsim-timeline-label {
        color: var(--cogsim-text-secondary);
    }

    /*
     * Current step
     */
    .cogsim-timeline-step.is-active
    .cogsim-timeline-point {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-primary);
        color: #FFFFFF;
    }

    .cogsim-timeline-step.is-active
    .cogsim-timeline-label {
        color: var(--cogsim-text);
        font-weight: 650;
    }

    /*
     * Upcoming steps
     */
    .cogsim-timeline-step.is-upcoming
    .cogsim-timeline-point {
        border-color: var(--cogsim-border-strong);
        background: var(--cogsim-surface);
        color: var(--cogsim-text-muted);
    }

    .cogsim-timeline-step.is-upcoming
    .cogsim-timeline-label {
        color: var(--cogsim-text-muted);
    }

    @media (max-width: 1180px) {
        .cogsim-workflow-timeline > .cogsim-timeline-step {
            flex-basis: 96px;
            min-width: 96px;
        }

        .cogsim-timeline-label {
            max-width: 7rem;
            font-size: 0.65rem;
        }
    }

    @media (max-width: 820px) {
        .cogsim-workflow-timeline > .cogsim-timeline-step {
            flex: 0 0 96px;
            min-width: 96px;
        }
    }
"""
