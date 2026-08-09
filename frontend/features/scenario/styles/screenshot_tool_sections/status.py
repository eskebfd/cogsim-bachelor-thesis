SCREENSHOT_STATUS_CSS = """
    /*
     * Main uploader text
     */

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"] p {
        margin: 0;

        color: var(--cogsim-text);
        font-size: 0.66rem;
        font-weight: 550;
        line-height: 1.35;
        text-align: center;
    }

    /*
     * File type and size information
     */

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzone"] small {
        display: block;

        margin: 0.1rem auto 0;

        color: var(--cogsim-text-muted);
        font-size: 0.6rem;
        font-weight: 400;
        line-height: 1.35;
        text-align: center;
    }

    :is(
        [class*="st-key-scenario_upload_panel"],
        [class*="st-key-scenario_task_screenshot_attachment"]
    )
    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: flex;
        width: 100%;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 0.35rem;

        margin: 0;
        padding: 0;

        text-align: center;
    }

    /*
     * Uploaded image card
     */

    [class*="st-key-uploaded_image_card"] {
        max-width: 860px;
        margin: 0.45rem auto 0.35rem;

        overflow: hidden;

        border: 1px solid var(--cogsim-border);
        border-radius: 16px;

        background:
            linear-gradient(
                180deg,
                rgba(251, 250, 255, 0.88) 0%,
                rgba(255, 255, 255, 0.98) 100%
            );
    }

"""
