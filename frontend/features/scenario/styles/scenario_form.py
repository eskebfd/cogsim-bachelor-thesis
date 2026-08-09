SCENARIO_FORM_CSS = """
    /*
     * Guided scenario fields
     */

    [class*="st-key-scenario_text_panel"] {
        margin-top: 0.35rem;
        padding: 0.95rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 16px;

        background: rgba(255, 255, 255, 0.86);
        box-shadow: 0 14px 42px rgba(38, 31, 84, 0.05);
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"] {
        margin-bottom: 0.9rem;
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"]:last-child {
        margin-bottom: 0;
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"] label {
        margin-bottom: 0.4rem;
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"] label p {
        margin: 0;

        color: var(--cogsim-text);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0;
        line-height: 1.35;
        text-transform: none;
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"] textarea {
        padding: 0.95rem 1rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 14px;

        background: var(--cogsim-surface);
        color: var(--cogsim-text);

        font-family:
            Inter,
            ui-sans-serif,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
        font-size: 0.9rem;
        font-weight: 400;
        line-height: 1.58;

        caret-color: var(--cogsim-primary);
        resize: vertical;

        transition:
            border-color 0.15s ease,
            background-color 0.15s ease,
            box-shadow 0.15s ease;
    }

    /*
     * Aufgabe
     */

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"]:has(
        textarea[aria-label="Aufgabe"]
    ) textarea {
        min-height: 105px;
    }

    /*
     * Interface
     */

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"]:has(
        textarea[aria-label="Interface"]
    ) textarea {
        min-height: 125px;
    }

    /*
     * Umgebung
     */

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"]:has(
        textarea[aria-label="Umgebung"]
    ) textarea {
        min-height: 125px;
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"] textarea:hover {
        border-color: var(--cogsim-border-strong);
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-surface);
        box-shadow: 0 0 0 3px var(--cogsim-primary-soft);
        outline: none;
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"] textarea::placeholder {
        color: var(--cogsim-text-muted);
        opacity: 1;
    }

    [class*="st-key-scenario_text_panel"]
    [data-testid="stTextArea"] textarea::selection {
        background: var(--cogsim-primary-soft);
    }
"""
