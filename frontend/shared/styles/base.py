BASE_CSS = """
        html, body, [class*="css"] {
            font-family:
                Inter, ui-sans-serif, system-ui, -apple-system,
                BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: var(--cogsim-text);
        }

        html {
            overflow-y: scroll;
            scrollbar-gutter: stable;
        }

        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            scrollbar-gutter: stable;
        }

        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(245, 246, 248, 0.75);
        }

        ::-webkit-scrollbar-thumb {
            border: 3px solid rgba(245, 246, 248, 0.75);
            border-radius: 999px;
            background: rgba(124, 77, 255, 0.34);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(124, 77, 255, 0.52);
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1140px;
            padding: 1rem 1.5rem 3rem;
        }

        h1, h2, h3, h4 {
            color: var(--cogsim-text);
            letter-spacing: -0.025em;
        }

        [class*="title"]:not([class*="badge"]):not([class*="tab"]),
        [class*="heading"],
        [class*="header__title"],
        [class*="section-title"] {
            color: var(--cogsim-text);
        }

        p,
        label,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] label {
            color: var(--cogsim-text-secondary);
        }

        [data-testid="stCaptionContainer"] {
            color: var(--cogsim-text-muted);
            line-height: 1.45;
        }
"""
