SCREENSHOT_SUMMARY_CSS = """
    /*
     * Header row
     */

    [class*="st-key-uploaded_image_card"]
    [data-testid="stHorizontalBlock"] {
        min-height: 0;
        align-items: center;

        margin: 0;
        padding: 0.55rem 0.65rem;
    }

    [class*="st-key-uploaded_image_card"]
    [data-testid="column"] {
        padding-top: 0;
        padding-bottom: 0;
    }

    .cogsim-uploaded-image__thumbnail {
        display: flex;
        height: 112px;
        align-items: center;
        justify-content: center;

        overflow: hidden;

        border: 1px solid var(--cogsim-border);
        border-radius: 12px;

        background: var(--cogsim-surface-muted);
    }

    .cogsim-uploaded-image__thumbnail img {
        display: block;
        max-width: 100%;
        max-height: 112px;
        width: auto;
        height: auto;

        object-fit: contain;
    }

    .cogsim-uploaded-image__meta {
        min-width: 0;
    }

    .cogsim-uploaded-image__status {
        display: inline-flex;
        align-items: center;

        margin-bottom: 0.25rem;
        padding: 0.18rem 0.45rem;

        border: 1px solid rgba(22, 138, 74, 0.24);
        border-radius: 999px;

        background: rgba(22, 138, 74, 0.08);
        color: var(--cogsim-success);

        font-size: 0.62rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .cogsim-uploaded-image__title {
        overflow: hidden;

        color: var(--cogsim-text);
        font-size: 0.76rem;
        font-weight: 600;
        line-height: 1.25;

        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /*
     * Remove icon
     */

    [class*="st-key-remove_scenario_image_icon"] {
        display: flex;
        align-items: center;
        justify-content: flex-end;

        margin: 0;
        padding: 0;
    }

    [class*="st-key-remove_scenario_image_icon"] button {
        display: inline-flex;
        width: 26px;
        min-width: 26px;
        height: 26px;
        min-height: 26px;
        align-items: center;
        justify-content: center;

        margin: 0;
        padding: 0;

        border: 0;
        border-radius: 50%;

        background: transparent;
        color: var(--cogsim-text-muted);

        font-size: 1rem;
        font-weight: 500;
        line-height: 1;

        box-shadow: none;
    }

    [class*="st-key-remove_scenario_image_icon"] button:hover {
        border: 0;
        background: var(--cogsim-surface-muted);
        color: var(--cogsim-text);
    }

    [class*="st-key-remove_scenario_image_icon"] button:focus {
        border: 0;
        box-shadow: 0 0 0 2px var(--cogsim-primary-soft);
    }

    /*
     * Footer
     */

    .cogsim-uploaded-image__footer {
        color: var(--cogsim-text-muted);
        font-size: 0.68rem;
        line-height: 1.25;
    }

"""
