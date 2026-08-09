RESULT_TIMELINE_CSS = """
    /*
    - Results timeline
     */

    [class*="st-key-simulation_timeline_panel"] {
        padding: 1.2rem 1.25rem 1.3rem;
        border: 1px solid var(--cogsim-border);
        border-radius: 22px;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.99), rgba(248, 250, 255, 0.92)),
            var(--cogsim-surface);
        box-shadow: 0 20px 48px rgba(38, 35, 80, 0.07);
    }

    [class*="st-key-simulation_timeline_panel"] h4 {
        margin: 0 0 0.15rem;
        color: var(--cogsim-text);
        font-size: 1.12rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    [class*="st-key-simulation_timeline_panel"] .cogsim-timeline-subtitle {
        margin: 0 0 0.85rem;
        color: var(--cogsim-text-secondary);
        font-size: 0.88rem;
        line-height: 1.5;
    }

    [class*="st-key-simulation_timeline_panel"] [data-testid="stSelectbox"] {
        max-width: 24rem;
        margin-bottom: 0.8rem;
    }

    [class*="st-key-simulation_timeline_panel"] [data-testid="stSelectbox"] label {
        color: var(--cogsim-text-secondary);
        font-size: 0.78rem;
        font-weight: 650;
    }

    [class*="st-key-simulation_timeline_panel"] [data-testid="stVegaLiteChart"] {
        padding: 0.2rem 0 0;
        border-radius: 18px;
        overflow: hidden;
    }
"""
