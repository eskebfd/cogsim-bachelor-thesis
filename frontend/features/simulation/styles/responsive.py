RESULT_RESPONSIVE_CSS = """
    @media (max-width: 1180px) {
        .cogsim-result-summary-primary-grid,
        .cogsim-result-summary-small-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .cogsim-explain-grid {
            grid-template-columns: 1fr;
        }

        .cogsim-explain-card__analysis {
            grid-template-columns: 1fr;
        }

        .cogsim-profile-comparison-grid,
        .cogsim-result-legend-grid,
        .cogsim-profile-kpi-grid,
        .cogsim-overview-context-grid,
        .cogsim-overview-action-grid,
        .cogsim-overview-time-grid,
        .cogsim-overview-recommendation-summary-grid,
        .cogsim-event-legend-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 680px) {
        .cogsim-result-summary-primary-grid,
        .cogsim-result-summary-small-grid {
            grid-template-columns: 1fr;
        }

        .cogsim-profile-comparison-grid,
        .cogsim-result-legend-grid,
        .cogsim-profile-kpi-grid,
        .cogsim-overview-context-grid,
        .cogsim-overview-action-grid,
        .cogsim-overview-time-grid,
        .cogsim-overview-recommendation-summary-grid,
        .cogsim-event-legend-grid {
            grid-template-columns: 1fr;
        }

        .cogsim-result-summary-header {
            align-items: flex-start;
            flex-direction: column;
            gap: 0.2rem;
        }

        .cogsim-explain-card__topline,
        .cogsim-explain-card__effect-row {
            align-items: flex-start;
            flex-direction: column;
        }
    }
"""
