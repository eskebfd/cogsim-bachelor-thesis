SCREENSHOT_CAPTURE_CSS = """
    /*
     * Drag-and-drop upload zone
     */

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"] {
        display: flex;
        min-height: 38px;
        align-items: center;
        justify-content: center;

        padding: 0.34rem 0.48rem;

        border: 1px dashed var(--cogsim-border-strong);
        border-radius: 10px;

        background: var(--cogsim-surface-muted);
        text-align: center;

        transition:
            border-color 0.15s ease,
            background-color 0.15s ease;
    }

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"] > div,
    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"] section {
        display: flex;
        width: 100%;
        height: 100%;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 0.48rem;

        margin: 0;
        padding: 0;

        text-align: center;
    }

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-primary-soft);
    }

    /*
     * Upload icon
     */

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"] svg {
        width: 18px;
        height: 18px;

        color: var(--cogsim-primary);
    }

    /*
     * Upload button
     */

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"] button {
        display: inline-flex;
        min-height: 28px;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;

        margin: 0 auto;
        padding: 0.34rem 0.56rem;

        border: 1px solid var(--cogsim-border);
        border-radius: 9px;

        background: var(--cogsim-surface);
        color: var(--cogsim-text);

        font-size: 0.62rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        line-height: 1.2;
        text-transform: uppercase;

        box-shadow: none;
    }

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"] button:hover {
        border-color: var(--cogsim-primary);
        background: var(--cogsim-primary-soft);
        color: var(--cogsim-primary);
    }

"""
