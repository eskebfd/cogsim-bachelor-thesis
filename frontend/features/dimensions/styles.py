DIMENSIONS_CSS = """
    /*
     * Intro
     */

    .cogsim-dimensions-intro {
        margin-bottom: 0.9rem;
        padding: 0.85rem 1rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface);
    }

    .cogsim-dimensions-intro__title {
        margin-bottom: 0.2rem;

        color: var(--cogsim-text);
        font-size: 0.86rem;
        font-weight: 650;
        line-height: 1.35;
    }

    .cogsim-dimensions-intro__text {
        color: var(--cogsim-text-secondary);
        font-size: 0.76rem;
        line-height: 1.4;
    }

    /*
     * Tabs
     */

    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.35rem;

        margin-bottom: 0.75rem;
        padding: 0.25rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 10px;

        background: var(--cogsim-surface-muted);
    }

    [data-testid="stTabs"] [data-baseweb="tab"] {
        min-height: 34px;

        padding: 0.4rem 0.75rem;

        border: 1px solid transparent;
        border-radius: 8px;

        background: transparent;
        color: var(--cogsim-text-secondary);

        font-size: 0.74rem;
        font-weight: 600;
        letter-spacing: 0.04em;

        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            color 0.15s ease,
            box-shadow 0.15s ease;
    }

    [data-testid="stTabs"] [data-baseweb="tab"]:hover {
        background: rgba(124, 77, 255, 0.05);
        color: var(--cogsim-text);
    }

    [data-testid="stTabs"] [aria-selected="true"] {
        background: var(--cogsim-primary-soft);
        border-color: rgba(124, 77, 255, 0.18);

        color: var(--cogsim-primary);
        font-weight: 700;

        box-shadow: 0 1px 3px rgba(124, 77, 255, 0.08);
    }

    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        display: none;
    }

    [data-testid="stTabs"] [data-baseweb="tab-border"] {
        display: none;
    }

    /*
     * Dimension cards
     */

    [class*="st-key-dimension_card_"] {
        min-height: 0;
        height: auto;

        margin-bottom: 0.8rem;
        padding: 0.88rem 0.95rem 0.95rem;

        overflow: visible;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface);
        box-shadow: 0 10px 26px rgba(17, 24, 39, 0.035);

        transition:
            border-color 0.15s ease,
            box-shadow 0.15s ease;
    }

    [class*="st-key-dimension_card_"] > div {
        height: auto !important;
        overflow: visible !important;
    }

    [class*="st-key-dimension_card_"]:hover {
        border-color: var(--cogsim-border-strong);
        box-shadow: var(--cogsim-shadow);
    }

    /*
     * Attribute heading
     */

    .cogsim-dimension-header__title {
        overflow: hidden;

        color: var(--cogsim-text);
        font-size: 0.84rem;
        font-weight: 680;
        line-height: 1.3;

        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .cogsim-dimension-header__value {
        min-width: 2rem;

        color: var(--cogsim-primary);
        font-size: 0.84rem;
        font-weight: 700;
        line-height: 1.2;
        text-align: right;
    }

    .cogsim-dimension-header__badge {
        padding: 0.22rem 0.5rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 999px;

        background: var(--cogsim-surface-muted);
        color: var(--cogsim-text-secondary);

        font-size: 0.64rem;
        font-weight: 600;
        line-height: 1.2;
        white-space: nowrap;
    }

    [class*="st-key-dimension_card_"] [data-testid="stPopover"] button {
        display: inline-flex;
        align-items: center;
        justify-content: center;

        min-height: 1.7rem;
        height: 1.7rem;
        width: auto;
        min-width: 0;
        padding: 0 0.62rem 0 0.5rem;

        border: 1px solid rgba(124, 77, 255, 0.18);
        border-radius: 8px;

        background: rgba(124, 77, 255, 0.055);
        color: var(--cogsim-primary);

        font-size: 0.68rem;
        font-weight: 700;
        line-height: 1;
    }

    [class*="st-key-dimension_card_"] [data-testid="stPopover"] {
        display: flex;
        justify-content: flex-start;

        margin-top: 0.56rem;
        padding-top: 0.42rem;

        border-top: 1px solid var(--cogsim-border);
    }

    [class*="st-key-dimension_card_"] [data-testid="stPopover"] button p {
        margin: 0;

        color: inherit;
        font-size: 0.68rem;
        font-weight: 700;
        line-height: 1;
        white-space: nowrap;
    }

    [class*="st-key-dimension_card_"] [data-testid="stPopover"] button:hover {
        border-color: rgba(124, 77, 255, 0.34);
        background: rgba(124, 77, 255, 0.12);
        color: var(--cogsim-primary);
    }

    /*
     * Slider
     */

    [class*="st-key-dimension_card_"]
    [data-testid="stSlider"] {
        margin-top: 0.05rem;
        margin-bottom: 0;
        padding: 0;
    }

    [class*="st-key-dimension_card_"]
    [data-testid="stSlider"] > div {
        padding-top: 0;
        padding-bottom: 0;
    }

    [class*="st-key-dimension_card_"]
    [data-baseweb="slider"] {
        margin-top: 0;
        margin-bottom: 0;
    }

    /*
     * Scale descriptions
     */

    .cogsim-dimension-scale {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.75rem;

        margin-top: -0.15rem;
        margin-bottom: 0.1rem;
    }

    .cogsim-dimension-scale__minimum,
    .cogsim-dimension-scale__maximum {
        max-width: 48%;

        color: var(--cogsim-text-muted);
        font-size: 0.62rem;
        line-height: 1.25;

        overflow-wrap: anywhere;
    }

    .cogsim-dimension-scale__maximum {
        text-align: right;
    }

    /*
     * Responsive layout
     */

    @media (max-width: 900px) {
        [class*="st-key-dimension_card_"] {
            min-height: 0;
        }

        .cogsim-dimension-header__badge {
            white-space: normal;
        }
    }
"""
