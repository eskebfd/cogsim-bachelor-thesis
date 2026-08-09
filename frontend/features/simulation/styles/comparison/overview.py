RESULT_COMPARISON_OVERVIEW_CSS = """
    .cogsim-overview-context-panel,
    .cogsim-overview-action-panel,
    .cogsim-overview-time-panel,
    .cogsim-overview-recommendation-summary {
        margin: 0 0 1.1rem;
        padding: 1.05rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 22px;

        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.99), rgba(250, 250, 255, 0.94)),
            var(--cogsim-surface);
        box-shadow: 0 18px 45px rgba(38, 35, 80, 0.06);
    }

    .cogsim-overview-context-panel__header,
    .cogsim-overview-action-panel__header,
    .cogsim-overview-time-panel__header {
        margin-bottom: 0.85rem;
    }

    .cogsim-overview-context-panel__header span,
    .cogsim-overview-action-panel__header span,
    .cogsim-overview-time-panel__header span {
        display: block;
        color: var(--cogsim-text);
        font-size: 1.06rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .cogsim-overview-context-panel__header p,
    .cogsim-overview-action-panel__header p,
    .cogsim-overview-time-panel__header p {
        max-width: 62rem;
        margin: 0.22rem 0 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.86rem;
        line-height: 1.5;
    }

    .cogsim-overview-time-grid {
        display: grid;
        grid-template-columns: 1.35fr repeat(2, minmax(0, 0.8fr));
        gap: 0.82rem;
        margin-bottom: 0.95rem;
    }

    .cogsim-overview-time-profile {
        padding: 0.9rem;
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 17px;
        background: rgba(255, 255, 255, 0.9);
    }

    .cogsim-overview-time-profile--primary {
        border-color: rgba(109, 93, 251, 0.22);
        background:
            radial-gradient(circle at 18% 0%, rgba(109, 93, 251, 0.14), transparent 38%),
            linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(244, 241, 255, 0.9));
        box-shadow: 0 16px 36px rgba(91, 91, 214, 0.1);
    }

    .cogsim-overview-time-profile span,
    .cogsim-overview-recommendation-summary-card strong {
        display: block;
        color: var(--cogsim-text);
        font-size: 0.86rem;
        font-weight: 790;
    }

    .cogsim-overview-time-profile strong {
        display: block;
        margin: 0.25rem 0 0.12rem;
        color: var(--cogsim-text);
        font-size: clamp(1.35rem, 2.3vw, 2.05rem);
        font-weight: 830;
        letter-spacing: -0.045em;
        line-height: 1.04;
    }

    .cogsim-overview-time-profile small,
    .cogsim-overview-recommendation-summary-card small {
        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        font-weight: 640;
        line-height: 1.35;
    }

    .cogsim-overview-recommendation-summary-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.82rem;
    }

    .cogsim-overview-recommendation-preview {
        display: flex;
        flex-direction: column;

        min-height: 16rem;
        height: 16rem;
        overflow: hidden;
        margin-bottom: 0.55rem;
        padding: 0.98rem;
        border: 1px solid rgba(109, 93, 251, 0.16);
        border-radius: 18px;
        background:
            radial-gradient(circle at 14% 0%, rgba(109, 93, 251, 0.1), transparent 34%),
            rgba(255, 255, 255, 0.92);
        box-shadow: 0 14px 32px rgba(38, 35, 80, 0.055);
    }

    .cogsim-overview-recommendation-preview div {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .cogsim-overview-recommendation-preview strong {
        color: var(--cogsim-text);
        font-size: 0.95rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .cogsim-overview-recommendation-preview div span {
        flex: 0 0 auto;
        padding: 0.2rem 0.48rem;
        border-radius: 999px;
        background: rgba(245, 243, 255, 0.9);
        color: var(--cogsim-primary);
        font-size: 0.68rem;
        font-weight: 760;
        white-space: nowrap;
    }

    .cogsim-overview-recommendation-preview small {
        display: block;
        margin-top: 0.3rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        font-weight: 650;
    }

    .cogsim-overview-recommendation-preview ul {
        display: grid;
        gap: 0.38rem;
        margin: 0.72rem 0 0.72rem;
        padding: 0;
        color: var(--cogsim-text);
        list-style: none;
    }

    .cogsim-overview-recommendation-preview li {
        position: relative;
        padding: 0.44rem 0.55rem 0.44rem 1.7rem;
        border: 1px solid rgba(226, 232, 240, 0.86);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.74);
        color: var(--cogsim-text);
        font-size: 0.78rem;
        font-weight: 720;
        line-height: 1.35;
    }

    .cogsim-overview-recommendation-preview li:nth-child(n+3) {
        display: none;
    }

    .cogsim-overview-recommendation-preview li::before {
        content: "";
        position: absolute;
        top: 0.82rem;
        left: 0.72rem;
        width: 0.38rem;
        height: 0.38rem;
        border-radius: 999px;
        background: var(--cogsim-primary);
    }

    .cogsim-overview-recommendation-step {
        display: grid;
        grid-template-columns: auto minmax(0, 1fr);
        gap: 0.52rem;
        align-items: flex-start;
        margin-top: auto;
        padding: 0.55rem 0.62rem;
        border: 1px solid rgba(109, 93, 251, 0.14);
        border-radius: 13px;
        background: rgba(245, 243, 255, 0.6);
    }

    .cogsim-overview-recommendation-step span {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 2.3rem;
        min-height: 1.35rem;
        padding: 0 0.42rem;
        border-radius: 999px;
        background: var(--cogsim-primary);
        color: white;
        font-size: 0.62rem;
        font-weight: 820;
        line-height: 1;
        white-space: nowrap;
    }

    .cogsim-overview-recommendation-step p {
        margin: 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        font-weight: 620;
        line-height: 1.35;
    }

    .cogsim-overview-recommendation-summary-card {
        padding: 0.95rem;
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 17px;
        background: rgba(255, 255, 255, 0.9);
    }

    .cogsim-overview-recommendation-summary-card span {
        display: block;
        margin-top: 0.32rem;
        color: var(--cogsim-primary);
        font-size: 1.65rem;
        font-weight: 830;
        letter-spacing: -0.04em;
        line-height: 1;
    }

    .cogsim-overview-recommendation-summary-card p {
        margin: 0.55rem 0 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        line-height: 1.4;
    }

    .cogsim-overview-context-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.92rem;
    }

    .cogsim-overview-context-card {
        min-height: 196px;
        padding: 1rem;

        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 18px;

        background: rgba(255, 255, 255, 0.9);
    }

    .cogsim-overview-context-card__icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.45rem;
        height: 2.45rem;
        margin-bottom: 0.68rem;
        border: 1px solid rgba(109, 93, 251, 0.16);
        border-radius: 14px;
        background: rgba(245, 243, 255, 0.78);
        color: var(--cogsim-primary);
    }

    .cogsim-overview-context-card__icon svg {
        width: 1.35rem;
        height: 1.35rem;
    }

    .cogsim-overview-context-card strong {
        display: block;
        color: var(--cogsim-text);
        font-size: 0.9rem;
        font-weight: 790;
        line-height: 1.25;
    }

    .cogsim-overview-context-card p {
        margin: 0.42rem 0 0.58rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.8rem;
        line-height: 1.46;
    }

    .cogsim-overview-context-card small {
        display: block;
        color: var(--cogsim-primary);
        font-size: 0.72rem;
        font-weight: 680;
        line-height: 1.35;
    }

    .cogsim-overview-context-card__chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.38rem;
        margin-top: 0.72rem;
    }

    .cogsim-overview-context-card__chips span {
        display: inline-flex;
        padding: 0.22rem 0.52rem;
        border: 1px solid rgba(109, 93, 251, 0.14);
        border-radius: 999px;
        background: rgba(245, 243, 255, 0.7);
        color: var(--cogsim-primary);
        font-size: 0.7rem;
        font-weight: 720;
        line-height: 1;
    }

    .cogsim-overview-context-card__event-list {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.32rem 0.7rem;
        margin: 0.72rem 0 0;
        padding: 0;
        list-style: none;
    }

    .cogsim-overview-context-card__event-list li {
        position: relative;
        padding-left: 0.8rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.74rem;
        font-weight: 650;
        line-height: 1.32;
    }

    .cogsim-overview-context-card__event-list li::before {
        position: absolute;
        top: 0.48em;
        left: 0;
        width: 0.34rem;
        height: 0.34rem;
        border-radius: 999px;
        background: var(--cogsim-primary);
        opacity: 0.46;
        content: "";
    }

    .cogsim-context-time-bars {
        display: grid;
        gap: 0.4rem;
        margin-top: 0.72rem;
    }

    .cogsim-context-time-row {
        display: grid;
        grid-template-columns: 5rem minmax(0, 1fr) auto;
        align-items: center;
        gap: 0.5rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        font-weight: 660;
    }

    .cogsim-context-time-row--basis {
        grid-template-columns: 5rem auto;
        color: var(--cogsim-text);
    }

    .cogsim-context-time-row__track {
        height: 0.42rem;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(226, 232, 240, 0.9);
    }

    .cogsim-context-time-row__track i {
        display: block;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #6D5DFB, #9B8CFF);
    }

    .cogsim-context-scale {
        margin-top: 0.72rem;
    }

    .cogsim-context-scale__track {
        height: 0.5rem;
        overflow: hidden;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(109, 93, 251, 0.16), rgba(109, 93, 251, 0.58));
    }

    .cogsim-context-scale__labels,
    .cogsim-context-scale__examples {
        display: flex;
        justify-content: space-between;
        gap: 0.5rem;
        margin-top: 0.42rem;
    }

    .cogsim-context-scale__examples {
        align-items: flex-start;
        flex-direction: column;
        margin-top: 0.7rem;
    }

    .cogsim-context-scale__examples span {
        color: var(--cogsim-text-secondary);
        font-size: 0.74rem;
        font-weight: 650;
        line-height: 1.3;
    }

    .cogsim-overview-action-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.86rem;
    }

    .cogsim-overview-action-card {
        padding: 1rem;

        border: 1px solid rgba(109, 93, 251, 0.16);
        border-radius: 18px;

        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 255, 0.88));
        box-shadow: 0 12px 28px rgba(38, 35, 80, 0.045);
    }

    .cogsim-overview-action-card__top {
        display: flex;
        align-items: center;
        gap: 0.46rem;
        margin-bottom: 0.2rem;
    }

    .cogsim-overview-action-card__top span {
        width: 0.68rem;
        height: 0.68rem;
        border-radius: 999px;
    }

    .cogsim-overview-action-card__top strong {
        color: var(--cogsim-text);
        font-size: 0.88rem;
        font-weight: 780;
    }

    .cogsim-overview-action-card > small {
        display: block;
        margin-bottom: 0.58rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.7rem;
        font-weight: 690;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .cogsim-overview-action-card .cogsim-explain-card__list {
        padding-left: 1.05rem;
        color: var(--cogsim-text);
        font-size: 0.82rem;
        line-height: 1.48;
    }

    .cogsim-overview-action-card__empty {
        margin: 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.8rem;
        line-height: 1.45;
    }

"""
