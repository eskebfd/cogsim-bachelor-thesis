SIDEBAR_CSS = """
    /*
     * Sidebar
     */

    .stSidebar {
        border-right: 1px solid var(--cogsim-border);
    }

    .cogsim-sidebar-section {
        margin-bottom: 1rem;
    }

    .cogsim-sidebar-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;

        margin-bottom: 1rem;

        color: var(--cogsim-text-secondary);

        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .cogsim-sidebar-title .cogsim-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: var(--cogsim-primary);
    }

    .stSidebar .stButton {
        margin-bottom: 0.5rem;
    }

    .stSidebar .stButton > button {
        display: flex;
        align-items: center;
        justify-content: flex-start;

        gap: 0.65rem;

        width: 100%;
        min-height: 42px;

        padding: 0.75rem 0.9rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface);
        color: var(--cogsim-text);

        transition:
            border-color 0.15s ease,
            background-color 0.15s ease,
            color 0.15s ease;
    }

    .stSidebar .stButton > button:hover {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);
    }

    .stSidebar .stButton > button p {
        margin: 0;
        color: inherit;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
"""
