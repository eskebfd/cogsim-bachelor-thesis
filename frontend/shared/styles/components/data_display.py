DATA_DISPLAY_CSS = """
        .review-box {
            background: var(--cogsim-surface-muted);
            border: 1px solid var(--cogsim-border);
            border-radius: 12px;
            padding: 0.55rem 0.7rem;
            color: var(--cogsim-text);
            font-size: 0.88rem;
            line-height: 1.45;
            margin: 0.25rem 0 0.65rem;
        }

        .review-badge {
            display: inline-flex;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            background: var(--cogsim-primary-soft);
            border: 1px solid #D9D2F3;
            color: var(--cogsim-primary);
            font-size: 0.8rem;
            font-weight: 700;
            margin: 0.25rem 0 0.65rem;
        }

        .review-label {
            color: var(--cogsim-text-secondary);
            font-size: 0.82rem;
            font-weight: 750;
            margin: 0.6rem 0 0.15rem;
        }

        .review-section-title {
            color: var(--cogsim-text);
            font-size: 0.92rem;
            font-weight: 750;
            margin: 0.8rem 0 0.35rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--cogsim-surface);
            border-color: var(--cogsim-border);
            border-radius: var(--cogsim-radius);
            box-shadow: none;
        }

        [data-testid="stDataFrame"] {
            color: var(--cogsim-text);
            background: var(--cogsim-surface);
            border: 1px solid var(--cogsim-border);
            border-radius: 14px;
            overflow: hidden;
        }

        .status-message {
            padding: 0.85rem 1rem;
            border-radius: 14px;
            margin: 0.5rem 0 1rem 0;
            font-size: 0.92rem;
            line-height: 1.45;
            border: 1px solid var(--cogsim-border);
        }

        .status-info {
            color: #1E3A8A;
            background: #EFF6FF;
            border-color: #BFDBFE;
        }

        .status-warning {
            color: #92400E;
            background: #FFFBEB;
            border-color: #FDE68A;
        }

        .status-success {
            color: #166534;
            background: #F0FDF4;
            border-color: #BBF7D0;
        }

        .status-error {
            color: #991B1B;
            background: #FEF2F2;
            border-color: #FECACA;
        }

        .cogsim-task-flow-intro {
            margin-bottom: 0.9rem;
            padding: 0.85rem 1rem;

            border: 1px solid var(--cogsim-border);
            border-radius: 12px;

            background: var(--cogsim-surface);
        }

        .cogsim-task-flow-intro__title {
            margin-bottom: 0.2rem;

            color: var(--cogsim-text);
            font-size: 0.86rem;
            font-weight: 650;
            line-height: 1.35;
        }

        .cogsim-task-flow-intro__text {
            color: var(--cogsim-text-secondary);
            font-size: 0.76rem;
            line-height: 1.4;
        }

        .stProgress > div > div > div > div {
            background: var(--cogsim-primary);
        }

        .stProgress > div > div > div {
            background: var(--cogsim-border);
        }
"""
