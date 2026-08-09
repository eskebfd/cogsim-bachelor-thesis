RESULT_EVENTS_CSS = """
    /*
    - Event legend
     */

    .cogsim-event-legend-panel {
        margin: 0 0 1.1rem;
        padding: 1.05rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 22px;

        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.99), rgba(250, 250, 255, 0.94)),
            var(--cogsim-surface);
        box-shadow: 0 18px 46px rgba(38, 35, 80, 0.065);
    }

    .cogsim-event-legend-panel--compact {
        margin-top: 0.65rem;
    }

    .cogsim-event-intro {
        margin: 0 0 0.95rem;
        padding: 0.9rem 1rem;

        border: 1px solid rgba(226, 232, 240, 0.92);
        border-radius: 17px;

        background: rgba(255, 255, 255, 0.78);
    }

    .cogsim-event-intro strong {
        display: block;

        color: var(--cogsim-text);
        font-size: 0.84rem;
        font-weight: 780;
    }

    .cogsim-event-intro p {
        margin: 0.35rem 0 0.5rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        line-height: 1.45;
    }

    .cogsim-event-intro__types {
        display: inline-flex;
        max-width: 100%;
        flex-wrap: wrap;
        gap: 0.28rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.7rem;
        font-weight: 760;
        line-height: 1.35;
    }

    .cogsim-event-icon-legend {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin: -0.2rem 0 0.9rem;
        padding: 0.65rem 0.72rem;
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.72);
    }

    .cogsim-event-icon-legend strong {
        margin-right: 0.12rem;
        color: var(--cogsim-text);
        font-size: 0.74rem;
        font-weight: 760;
    }

    .cogsim-event-icon-legend__item {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        min-height: 1.55rem;
        padding: 0.18rem 0.48rem;
        border: 1px solid rgba(109, 93, 251, 0.16);
        border-radius: 999px;
        background: rgba(245, 243, 255, 0.78);
    }

    .cogsim-event-icon-legend__item i {
        display: inline-flex;
        min-width: 0.6rem;
        color: var(--cogsim-primary);
        font-size: 0.7rem;
        font-style: normal;
        font-weight: 820;
        line-height: 1;
    }

    .cogsim-event-icon-legend__item b {
        color: var(--cogsim-text-secondary);
        font-size: 0.68rem;
        font-weight: 700;
    }

    .cogsim-event-profile-section {
        padding: 0.9rem 0 0;
    }

    .cogsim-event-profile-section + .cogsim-event-profile-section {
        margin-top: 0.9rem;
        border-top: 1px solid rgba(226, 232, 240, 0.82);
    }

    .cogsim-event-profile-section__header {
        display: flex;
        align-items: center;
        gap: 0.45rem;

        margin-bottom: 0.7rem;
    }

    .cogsim-event-profile-section__header strong {
        color: var(--cogsim-text);
        font-size: 0.84rem;
        font-weight: 780;
    }

    .cogsim-event-profile-section__header small {
        margin-left: auto;
        padding: 0.16rem 0.48rem;

        border: 1px solid rgba(109, 93, 251, 0.16);
        border-radius: 999px;

        background: rgba(238, 242, 255, 0.65);
        color: var(--cogsim-primary);
        font-size: 0.66rem;
        font-weight: 760;
    }

    .cogsim-event-profile-section__empty {
        margin: 0;

        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        line-height: 1.4;
    }

    .cogsim-event-legend-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.78rem;
    }

    .cogsim-event-legend-card {
        min-height: 0;
        padding: 0.9rem;

        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 17px;

        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 10px 22px rgba(38, 35, 80, 0.035);
    }

    .cogsim-event-legend-card--danger {
        border-color: rgba(226, 232, 240, 0.95);
        background: rgba(255, 255, 255, 0.9);
    }

    .cogsim-event-legend-card--warning {
        border-color: rgba(226, 232, 240, 0.95);
        background: rgba(255, 255, 255, 0.9);
    }

    .cogsim-event-legend-card--notice {
        border-color: rgba(226, 232, 240, 0.95);
        background: rgba(255, 255, 255, 0.9);
    }

    .cogsim-event-step-group {
        padding: 0.82rem;
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 17px;
        background: rgba(255, 255, 255, 0.72);
    }

    .cogsim-event-step-group + .cogsim-event-step-group {
        margin-top: 0.65rem;
    }

    .cogsim-event-step-group__header {
        display: grid;
        grid-template-columns: auto minmax(0, auto);
        justify-content: start;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.55rem;
    }

    .cogsim-event-step-group__header span,
    .cogsim-event-step-group__header small {
        padding: 0.18rem 0.48rem;
        border-radius: 999px;
        background: rgba(245, 243, 255, 0.82);
        color: var(--cogsim-primary);
        font-size: 0.66rem;
        font-weight: 760;
        white-space: nowrap;
    }

    .cogsim-event-step-group__header strong {
        color: var(--cogsim-text);
        font-size: 0.78rem;
        font-weight: 760;
        line-height: 1.25;
    }

    .cogsim-event-legend-card__top {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin-bottom: 0.3rem;
    }

    .cogsim-event-legend-card__dot {
        flex: 0 0 auto;
        width: 0.58rem;
        height: 0.58rem;

        border-radius: 999px;
    }

    .cogsim-event-legend-card__step {
        display: block;
        margin-bottom: 0.45rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        font-weight: 640;
        line-height: 1.35;
    }

    .cogsim-event-legend-card strong {
        color: var(--cogsim-text);
        font-size: 0.84rem;
        font-weight: 780;
        line-height: 1.2;
    }

    .cogsim-event-legend-card__meta {
        margin-top: 0.35rem;

        color: var(--cogsim-primary);
        font-size: 0.7rem;
        font-weight: 720;
    }

    .cogsim-event-legend-card p {
        margin: 0.45rem 0 0;

        color: var(--cogsim-text);
        font-size: 0.78rem;
        line-height: 1.42;
    }

    .cogsim-event-legend-card__facts {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.45rem;
        margin-top: 0.7rem;
    }

    .cogsim-event-legend-card small {
        display: block;
        margin: 0;
        padding: 0.52rem 0.58rem;

        border: 1px solid rgba(226, 232, 240, 0.88);
        border-radius: 12px;
        background: rgba(248, 250, 252, 0.86);

        color: var(--cogsim-text-secondary);
        font-size: 0.7rem;
        font-weight: 640;
        line-height: 1.32;
    }

    .cogsim-event-legend-card small span {
        display: block;
        margin-bottom: 0.16rem;
        color: var(--cogsim-text);
        font-size: 0.64rem;
        font-weight: 780;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .cogsim-event-abort-card {
        margin-bottom: 0.75rem;
        padding: 0.82rem 0.9rem;

        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 15px;

        background: rgba(255, 255, 255, 0.84);
    }

    .cogsim-event-abort-card strong {
        color: var(--cogsim-text);
        font-size: 0.82rem;
        font-weight: 780;
    }

    .cogsim-event-abort-card p {
        margin: 0.35rem 0 0;

        color: var(--cogsim-text);
        font-size: 0.78rem;
        line-height: 1.45;
    }
"""
