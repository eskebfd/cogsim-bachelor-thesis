BUTTONS_CSS = """
    .stButton > button {
        border-radius: 12px;
        border: 1px solid var(--cogsim-border);
        background: var(--cogsim-surface);
        color: var(--cogsim-text);

        min-height: 40px;
        padding: 0.55rem 0.9rem;

        font-size: 0.75rem;
        font-weight: 600;
        line-height: 1.2;
        letter-spacing: 0.08em;
        text-transform: uppercase;

        box-shadow: none;

        transition:
            border-color 0.15s ease,
            background-color 0.15s ease,
            color 0.15s ease,
            transform 0.15s ease;
    }

    /*
     * Streamlit rendert den Buttontext je nach Version
     * unterschiedlich (p, span oder div).
     * Deshalb werden alle Kindelemente vereinheitlicht.
     */
    .stButton > button *,
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        margin: 0;

        color: inherit !important;

        font-size: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
        letter-spacing: inherit !important;
        text-transform: inherit !important;
    }

    .stButton > button:hover {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);
    }

    /*
     * Primary Buttons
     */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: var(--cogsim-primary);
        border-color: var(--cogsim-primary);
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"] *,
    .stButton > button[data-testid="baseButton-primary"] * {
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: var(--cogsim-primary-hover);
        border-color: var(--cogsim-primary-hover);
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"]:hover *,
    .stButton > button[data-testid="baseButton-primary"]:hover * {
        color: #FFFFFF !important;
    }

    .stButton > button:disabled {
        background: #F4F2FA;
        border-color: var(--cogsim-border);
        color: var(--cogsim-text-muted);
        transform: none;
    }

    .stButton > button:disabled * {
        color: inherit !important;
    }
"""
