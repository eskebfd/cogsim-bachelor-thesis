from frontend.shared.ui.loading_overlay import render_global_loading_overlay


def render_loading_progress(
    message: str,
    *,
    hint: str | None = None,
    estimated_seconds: float | None = None,
):
    """Compatibility wrapper for the global loading overlay."""
    return render_global_loading_overlay(
        message,
        hint=hint,
        estimated_seconds=estimated_seconds,
    )
