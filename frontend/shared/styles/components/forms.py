FORMS_CSS = """
        section[data-testid="stSidebar"] {
            background: var(--cogsim-surface);
            border-right: 1px solid var(--cogsim-border);
        }

        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            margin-top: 0.45rem;
        }

        [data-testid="stTextArea"] textarea,
        [data-testid="stTextInput"] input,
        [data-testid="stFileUploader"] {
            border-radius: 14px;
        }

        div[data-baseweb="select"] > div {
            border-radius: 12px;
            border-color: var(--cogsim-border);
            background: var(--cogsim-surface);
        }
"""
