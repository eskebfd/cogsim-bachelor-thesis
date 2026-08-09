HOME_CSS = """
    .cogsim-home-hero {
        max-width: 760px;
        padding: 0.1rem 0 1.35rem;
    }

    .cogsim-home-eyebrow {
        margin-bottom: 0.8rem;
        color: var(--cogsim-primary);
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .cogsim-home-title {
        max-width: 720px;
        margin: 0;
        color: var(--cogsim-text);
        font-size: clamp(2.3rem, 5vw, 4.5rem);
        font-weight: 720;
        line-height: 1.02;
        letter-spacing: -0.045em;
    }

    .cogsim-home-lead {
        max-width: 700px;
        margin: 1.25rem 0 0;
        color: var(--cogsim-text);
        font-size: 1.05rem;
        line-height: 1.65;
    }

    .cogsim-home-description {
        max-width: 680px;
        margin: 0.8rem 0 0;
        color: var(--cogsim-text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .cogsim-home-step {
        min-height: 130px;
        padding: 0.9rem 0;
        border-top: 1px solid var(--cogsim-border);
    }

    .cogsim-home-step__number {
        margin-bottom: 1rem;
        color: var(--cogsim-text-muted);
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
    }

    .cogsim-home-step__title {
        color: var(--cogsim-text);
        font-size: 0.95rem;
        font-weight: 650;
        line-height: 1.3;
    }

    .cogsim-home-step__description {
        margin-top: 0.45rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.82rem;
        line-height: 1.5;
    }

    @media (max-width: 900px) {
        .cogsim-home-hero {
            padding-top: 0;
        }

        .cogsim-home-title {
            font-size: 2.6rem;
        }

        .cogsim-home-step {
            min-height: auto;
        }
    }
"""
