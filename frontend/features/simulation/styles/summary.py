RESULT_SUMMARY_CSS = """
    /*
    - Result highlights
     */

    .cogsim-result-summary-panel {
        margin: 0 0 1.1rem;
        padding: 1.15rem;
        border: 1px solid var(--cogsim-border);
        border-radius: 24px;
        background:
            radial-gradient(circle at 8% 0%, rgba(91, 91, 214, 0.08), transparent 34%),
            linear-gradient(135deg, rgba(255, 255, 255, 0.99), rgba(248, 250, 255, 0.94)),
            var(--cogsim-surface);
        box-shadow: 0 24px 58px rgba(38, 35, 80, 0.08);
    }

    .cogsim-result-summary-panel--danger,
    .cogsim-result-summary-panel--critical {
        border-color: rgba(220, 38, 38, 0.18);
        background:
            radial-gradient(circle at 8% 0%, rgba(220, 38, 38, 0.08), transparent 34%),
            linear-gradient(135deg, rgba(255, 255, 255, 0.99), rgba(255, 247, 247, 0.92)),
            var(--cogsim-surface);
    }

    .cogsim-result-summary-panel--warning,
    .cogsim-result-summary-panel--notice {
        border-color: rgba(217, 119, 6, 0.18);
        background:
            radial-gradient(circle at 8% 0%, rgba(217, 119, 6, 0.08), transparent 34%),
            linear-gradient(135deg, rgba(255, 255, 255, 0.99), rgba(255, 251, 235, 0.9)),
            var(--cogsim-surface);
    }

    .cogsim-result-summary-header {
        display: block;
        margin-bottom: 0.95rem;
    }

    .cogsim-result-summary-header span {
        color: var(--cogsim-text);
        font-size: 1.08rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .cogsim-result-summary-header small {
        display: block;
        max-width: 64rem;
        margin-top: 0.18rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.84rem;
        font-weight: 560;
        line-height: 1.5;
    }

    .cogsim-result-summary-primary-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(22rem, 0.82fr);
        gap: 0.9rem;
    }

    .cogsim-result-status-card,
    .cogsim-result-time-card {
        min-height: 184px;
        padding: 1.05rem;
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.94);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }

    .cogsim-result-status-card {
        display: grid;
        grid-template-columns: auto 1fr;
        align-items: flex-start;
        gap: 0.9rem;
    }

    .cogsim-result-status-card__icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 3.35rem;
        height: 3.35rem;
        border-radius: 999px;
        background: var(--cogsim-primary-soft);
        border: 1px solid rgba(109, 93, 251, 0.18);
        color: var(--cogsim-primary);
        box-shadow: 0 10px 24px rgba(91, 91, 214, 0.12);
    }

    .cogsim-result-status-card span,
    .cogsim-result-time-card span {
        display: block;
        color: var(--cogsim-primary);
        font-size: 0.72rem;
        font-weight: 780;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .cogsim-result-status-card h4 {
        margin: 0.25rem 0 0.55rem;
        color: var(--cogsim-text);
        font-size: 1.28rem;
        font-weight: 820;
        letter-spacing: -0.03em;
        line-height: 1.14;
    }

    .cogsim-result-status-card p,
    .cogsim-result-time-card p {
        margin: 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.9rem;
        line-height: 1.52;
    }

    .cogsim-result-status-card small {
        display: inline-block;
        margin-top: 0.7rem;
        padding: 0.28rem 0.5rem;
        border-radius: 999px;
        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);
        font-size: 0.72rem;
        font-weight: 700;
    }

    .cogsim-result-status-card--danger .cogsim-result-status-card__icon {
        background: rgba(220, 38, 38, 0.08);
        border-color: rgba(220, 38, 38, 0.2);
        color: var(--cogsim-danger);
    }

    .cogsim-result-status-card--warning .cogsim-result-status-card__icon,
    .cogsim-result-status-card--notice .cogsim-result-status-card__icon {
        background: rgba(217, 119, 6, 0.08);
        border-color: rgba(217, 119, 6, 0.2);
        color: #B45309;
    }

    .cogsim-result-status-card--success .cogsim-result-status-card__icon {
        background: rgba(22, 163, 74, 0.08);
        border-color: rgba(22, 163, 74, 0.2);
        color: var(--cogsim-success);
    }

    .cogsim-result-time-card strong {
        display: block;
        margin: 0.32rem 0 0.24rem;
        color: var(--cogsim-text);
        font-size: clamp(2rem, 4vw, 2.85rem);
        font-weight: 830;
        letter-spacing: -0.05em;
        line-height: 1;
    }

    .cogsim-result-time-card > small {
        display: block;
        margin-bottom: 0.75rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        line-height: 1.35;
    }

    .cogsim-result-time-card__basis {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.65rem;
        margin: 0.85rem 0;
    }

    .cogsim-result-time-card__basis div {
        padding: 0.72rem;
        border: 1px solid rgba(109, 93, 251, 0.12);
        border-radius: 14px;
        background:
            linear-gradient(180deg, rgba(241, 238, 255, 0.95), rgba(246, 244, 255, 0.85));
    }

    .cogsim-result-time-card__basis span {
        color: var(--cogsim-text-secondary);
        font-size: 0.65rem;
    }

    .cogsim-result-time-card__basis b {
        display: block;
        margin-top: 0.15rem;
        color: var(--cogsim-text);
        font-size: 0.86rem;
    }

    .cogsim-result-summary-small-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.85rem;
        margin-top: 0.9rem;
    }

    .cogsim-result-summary-small-card {
        min-height: 132px;
        padding: 0.92rem;
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.88);
    }

    .cogsim-result-summary-small-card span {
        display: block;
        color: var(--cogsim-text-secondary);
        font-size: 0.72rem;
        font-weight: 760;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .cogsim-result-summary-small-card strong {
        display: block;
        margin-top: 0.2rem;
        color: var(--cogsim-text);
        font-size: 1.28rem;
        font-weight: 790;
        line-height: 1.1;
        letter-spacing: -0.03em;
    }

    .cogsim-result-summary-small-card small {
        display: block;
        margin-top: 0.35rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.76rem;
        font-weight: 560;
        line-height: 1.3;
    }

    .cogsim-result-summary-small-card p {
        margin: 0.45rem 0 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.76rem;
        line-height: 1.4;
    }
"""
