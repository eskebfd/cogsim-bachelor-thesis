USER_PROFILES_CSS = """
    /*
     * Intro
     */

    .cogsim-user-profiles-intro {
        margin-bottom: 0.9rem;
        padding: 0.85rem 1rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface);
    }

    .cogsim-user-profiles-intro__title {
        margin-bottom: 0.2rem;

        color: var(--cogsim-text);
        font-size: 0.86rem;
        font-weight: 650;
        line-height: 1.35;
    }

    .cogsim-user-profiles-intro__text {
        color: var(--cogsim-text-secondary);
        font-size: 0.76rem;
        line-height: 1.4;
    }

    /*
     * User profile selection
     *
     * Each profile consists of:
     * 1. Main information card
     * 2. Attached footer/action area
     */

    [class*="st-key-profile_option_"] {
        width: 100%;
    }

    /*
     * Remove Streamlit spacing between the information card
     * and its attached footer/button.
     */
    [class*="st-key-profile_option_"] > div {
        gap: 0 !important;
    }

    [class*="st-key-profile_option_"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    .cogsim-profile-card__content {
        position: relative;
        display: flex;
        min-height: 182px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.7rem;

        padding: 1.55rem 1.25rem 1.4rem;

        background: var(--cogsim-surface);
        border: 1px solid var(--cogsim-border);
        border-bottom: 0;
        border-radius: 16px 16px 0 0;

        color: var(--cogsim-text);
        text-align: center;

        box-shadow: 0 10px 24px rgba(41, 37, 74, 0.05);
    }

    .cogsim-profile-card__content.is-selected {
        background: var(--cogsim-primary-soft);
        border-color: var(--cogsim-primary);
    }

    /*
     * Profile icon
     */
    .cogsim-profile-card__icon {
        display: flex;
        width: 48px;
        height: 48px;
        align-items: center;
        justify-content: center;

        margin-bottom: 0.15rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface-muted);
        color: var(--cogsim-primary);
    }

    .cogsim-profile-card__icon .cogsim-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: inherit;
    }

    .cogsim-profile-card__icon svg {
        display: block;
        color: inherit;
        stroke: currentColor;
    }

    /*
     * Profile title and description
     */
    .cogsim-profile-card__title {
        color: var(--cogsim-text);
        font-size: 1.08rem;
        font-weight: 600;
        line-height: 1.2;
    }

    .cogsim-profile-card__description {
        max-width: 15rem;

        color: var(--cogsim-text-secondary);
        font-size: 0.88rem;
        font-weight: 400;
        line-height: 1.45;
    }

    /*
     * Selected-state marker
     */
    .cogsim-profile-card__check {
        position: absolute;
        top: 0.8rem;
        right: 0.8rem;

        display: inline-flex;
        width: 22px;
        height: 22px;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background: var(--cogsim-primary);
        color: #FFFFFF;
    }

    .cogsim-profile-card__check .cogsim-icon {
        display: inline-flex;
        color: inherit;
    }

    .cogsim-profile-card__check svg {
        display: block;
        stroke: currentColor;
    }

    /*
     * Static footer for the Generic baseline profile.
     */
    .cogsim-profile-card__footer {
        display: flex;
        min-height: 44px;
        align-items: center;
        justify-content: center;

        margin: 0;
        padding: 0.55rem 0.9rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 0 0 16px 16px;

        background: var(--cogsim-surface-muted);
        color: var(--cogsim-text-secondary);

        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        line-height: 1.2;
        text-align: center;
        text-transform: uppercase;
    }

    [class*="st-key-profile_option_"][class*="_selected"]
    .cogsim-profile-card__footer {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);
    }

    /*
     * ADHS/Dyslexie footer button
     */
    [class*="st-key-profile_option_"] .stButton {
        margin: 0 !important;
    }

    [class*="st-key-profile_option_"] .stButton > button {
        min-height: 44px;
        width: 100%;

        margin: 0;
        padding: 0.55rem 0.9rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 0 0 16px 16px;

        background: var(--cogsim-surface-muted);
        color: var(--cogsim-text-secondary);

        font-size: 0.75rem !important;
        font-weight: 720 !important;
        letter-spacing: 0.08em;
        line-height: 1.2;
        text-transform: uppercase;

        box-shadow: none;

        transition:
            border-color 0.15s ease,
            background-color 0.15s ease,
            color 0.15s ease;
    }

    [class*="st-key-profile_option_"] .stButton > button:hover {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);
    }

    [class*="st-key-profile_option_"][class*="_selected"]
    .stButton > button {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-primary);
        color: #FFFFFF !important;
    }

    [class*="st-key-profile_option_"][class*="_selected"]
    .stButton > button:hover {
        border-color: var(--cogsim-primary-hover);
        background: var(--cogsim-primary-hover);
        color: #FFFFFF !important;
    }

    [class*="st-key-profile_option_"] .stButton > button p {
        margin: 0;
        font-size: 0.75rem !important;
        font-weight: 720 !important;
        letter-spacing: 0.075em !important;
        line-height: 1.2 !important;
        text-transform: uppercase;
        color: inherit !important;
    }

    [class*="st-key-profile_option_"][class*="_selected"]
    .stButton > button p {
        color: #FFFFFF !important;
    }

    /*
     * Responsive profile layout
     */
    @media (max-width: 900px) {
        .cogsim-profile-card__content {
            min-height: 160px;
        }
    }
"""
