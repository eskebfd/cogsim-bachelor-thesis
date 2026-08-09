SCREENSHOT_RESPONSIVE_CSS = """
    /*
     * Responsive layout
     */

    @media (max-width: 900px) {
        :is(
            [class*="st-key-scenario_upload_panel"],
            [class*="st-key-scenario_task_screenshot_attachment"]
        )
        [data-testid="stFileUploaderDropzone"] {
            min-height: 125px;
        }

        .cogsim-uploaded-image__thumbnail {
            height: 96px;
        }

        .cogsim-uploaded-image__thumbnail img {
            max-height: 96px;
        }

        [class*="st-key-screenshot_analysis_result"] {
            padding: 0.7rem;
        }

        .cogsim-screenshot-summary-grid {
            grid-template-columns: 1fr;
        }
    }
"""
