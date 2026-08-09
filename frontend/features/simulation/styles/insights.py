RESULT_INSIGHTS_CSS = """
    /*
    - Explainable profile insights
     */

    .cogsim-explain-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0.7rem 0 1.15rem;
    }

    .cogsim-explain-card {
        padding: 0.92rem;
        border: 1px solid var(--cogsim-border);
        border-radius: 18px;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(250, 250, 255, 0.92)),
            var(--cogsim-surface);
        box-shadow: 0 14px 34px rgba(38, 35, 80, 0.06);
    }

    .cogsim-explain-card--insight {
        border-color: rgba(217, 119, 6, 0.18);
    }

    .cogsim-explain-card--recommendation {
        border-color: rgba(109, 93, 251, 0.18);
    }

    .cogsim-explain-card--positive {
        border-color: rgba(22, 163, 74, 0.18);
    }

    .cogsim-explain-card__eyebrow {
        margin: 0;
        color: var(--cogsim-primary);
        font-size: 0.68rem;
        font-weight: 760;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .cogsim-explain-card__topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.7rem;
        margin-bottom: 0.42rem;
    }

    .cogsim-explain-card__badges {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-end;
        gap: 0.35rem;
    }

    .cogsim-explain-card__badge {
        display: inline-flex;
        align-items: center;
        min-height: 1.35rem;
        padding: 0.18rem 0.46rem;
        border: 1px solid rgba(109, 93, 251, 0.16);
        border-radius: 999px;
        background: rgba(245, 243, 255, 0.82);
        color: var(--cogsim-primary);
        font-size: 0.68rem;
        font-weight: 720;
        line-height: 1;
    }

    .cogsim-explain-card h5 {
        margin: 0 0 0.75rem;
        color: var(--cogsim-text);
        font-size: 0.98rem;
        font-weight: 780;
        letter-spacing: -0.02em;
        line-height: 1.25;
    }

    .cogsim-explain-card__step-box {
        display: grid;
        grid-template-columns: auto minmax(0, 1fr);
        align-items: center;
        gap: 0.6rem;
        margin: -0.25rem 0 0.75rem;
        padding: 0.58rem 0.68rem;
        border: 1px solid rgba(109, 93, 251, 0.16);
        border-radius: 14px;
        background: rgba(245, 243, 255, 0.68);
    }

    .cogsim-explain-card__step-box span {
        display: inline-grid;
        place-items: center;
        min-width: 3.1rem;
        min-height: 1.55rem;
        padding: 0 0.46rem;
        border-radius: 999px;
        background: var(--cogsim-primary);
        color: white;
        font-size: 0.68rem;
        font-weight: 820;
        line-height: 1;
        white-space: nowrap;
    }

    .cogsim-explain-card__step-box p {
        margin: 0;
        color: var(--cogsim-text);
        font-size: 0.78rem;
        font-weight: 640;
        line-height: 1.35;
    }

    .cogsim-explain-card__analysis {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.75rem;
        margin-top: 0.15rem;
    }

    .cogsim-explain-card__section {
        margin-top: 0.6rem;
    }

    .cogsim-explain-card__section span {
        display: block;
        margin-bottom: 0.15rem;
        color: var(--cogsim-text);
        font-size: 0.76rem;
        font-weight: 720;
    }

    .cogsim-explain-card__section p {
        margin: 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.82rem;
        line-height: 1.45;
    }

    .cogsim-explain-card__example {
        margin-top: 0.75rem;
        padding: 0.82rem 0.9rem;
        border: 1px solid rgba(109, 93, 251, 0.16);
        border-radius: 14px;
        background:
            linear-gradient(135deg, rgba(238, 242, 255, 0.95), rgba(245, 243, 255, 0.86));
        color: var(--cogsim-text);
        font-size: 0.84rem;
        font-weight: 560;
        line-height: 1.4;
    }

    .cogsim-explain-card__example span {
        display: block;
        margin-bottom: 0.25rem;
        color: var(--cogsim-primary);
        font-size: 0.72rem;
        font-weight: 820;
        letter-spacing: 0.07em;
        text-transform: uppercase;
    }

    .cogsim-explain-card__example p {
        margin: 0;
    }

    .cogsim-explain-card__list {
        margin: 0;
        padding-left: 1rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.82rem;
        line-height: 1.45;
    }

    .cogsim-explain-card__example .cogsim-explain-card__list {
        color: var(--cogsim-text);
        font-weight: 650;
    }

    .cogsim-explain-card__effect-row {
        display: flex;
        align-items: baseline;
        gap: 0.45rem;
        margin-top: 0.72rem;
        padding-top: 0.65rem;
        border-top: 1px solid rgba(226, 232, 240, 0.86);
    }

    .cogsim-explain-card__effect-row span {
        flex: 0 0 auto;
        color: var(--cogsim-text);
        font-size: 0.72rem;
        font-weight: 760;
    }

    .cogsim-explain-card__effect-row p {
        margin: 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        line-height: 1.35;
    }

    [class*="st-key-recommendation_priority_filter_"] {
        margin: 0.2rem 0 0.7rem;
        padding: 0.24rem;
        border: 1px solid rgba(226, 232, 240, 0.88);
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.74);
    }

    [class*="st-key-recommendation_priority_filter_"] [data-testid="stRadio"] > div {
        gap: 0.28rem;
    }

    [class*="st-key-recommendation_priority_filter_"] label {
        min-height: 1.95rem;
        padding: 0.34rem 0.64rem;
        border: 1px solid transparent;
        border-radius: 10px;
        color: var(--cogsim-text-secondary);
        font-size: 0.74rem;
        font-weight: 720;
    }

    [class*="st-key-recommendation_priority_filter_"] input[type="radio"],
    [class*="st-key-recommendation_priority_filter_"] [data-baseweb="radio"] > div:first-child {
        display: none;
    }

    [class*="st-key-recommendation_priority_filter_"] label:has(input:checked) {
        border-color: rgba(109, 93, 251, 0.18);
        background: rgba(245, 243, 255, 0.9);
        color: var(--cogsim-primary);
        box-shadow: 0 1px 4px rgba(109, 93, 251, 0.08);
    }
"""
