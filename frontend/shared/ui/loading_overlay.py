from contextlib import contextmanager
from html import escape
from time import monotonic, sleep
from typing import Iterator

import streamlit as st


def _format_estimated_duration(seconds: float) -> str:
    rounded_seconds = max(1, int(round(seconds)))
    if rounded_seconds < 60:
        return f"etwa {rounded_seconds} Sekunden"

    minutes = rounded_seconds // 60
    remaining_seconds = rounded_seconds % 60
    if remaining_seconds:
        return f"etwa {minutes} Minuten {remaining_seconds} Sekunden"
    return f"etwa {minutes} Minuten"


def render_global_loading_overlay(
    message: str,
    *,
    hint: str | None = None,
    estimated_seconds: float | None = None,
):
    placeholder = st.empty()
    safe_message = escape(message)
    safe_hint = escape(
        hint or "Die Verarbeitung kann einen Moment dauern."
    )
    duration_seconds = max(1.0, float(estimated_seconds or 18.0))
    safe_estimate = escape(_format_estimated_duration(duration_seconds))
    progress_style = (
        f"--cogsim-loading-duration: {duration_seconds:.1f}s;"
    )

    placeholder.markdown(
        (
            '<div class="cogsim-loading-overlay" aria-live="polite" '
            'aria-busy="true">'
            f'<div class="cogsim-loading-overlay__panel" style="{progress_style}">'
            '<div class="cogsim-loading-overlay__mascot-track" aria-hidden="true">'
            '<div class="cogsim-loading-overlay__mascot">'
            '<span class="cogsim-pixel-dino">'
            '<span class="cogsim-pixel-dino__body"></span>'
            '<span class="cogsim-pixel-dino__head"></span>'
            '<span class="cogsim-pixel-dino__tail"></span>'
            '<span class="cogsim-pixel-dino__leg cogsim-pixel-dino__leg--front"></span>'
            '<span class="cogsim-pixel-dino__leg cogsim-pixel-dino__leg--back"></span>'
            '<span class="cogsim-pixel-dino__eye"></span>'
            "</span>"
            "</div>"
            "</div>"
            f'<div class="cogsim-loading-overlay__message">{safe_message}</div>'
            '<div class="cogsim-loading-overlay__estimate">'
            f"Geschätzte Dauer: {safe_estimate}"
            "</div>"
            '<div class="cogsim-loading-overlay__progress" role="progressbar" '
            'aria-label="Geschätzter Fortschritt" '
            '>'
            '<div class="cogsim-loading-overlay__progress-bar"></div>'
            "</div>"
            '<div class="cogsim-loading-overlay__hint">'
            f"{safe_hint}"
            "</div>"
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    return placeholder


def clear_stale_global_loading_overlay() -> None:
    st.markdown(
        (
            "<style>"
            ".cogsim-loading-overlay {"
            "display: none !important;"
            "pointer-events: none !important;"
            "}"
            "</style>"
        ),
        unsafe_allow_html=True,
    )


@contextmanager
def global_loading(
    message: str,
    *,
    hint: str | None = None,
    min_visible_seconds: float = 0.0,
    estimated_seconds: float | None = None,
) -> Iterator[None]:
    started_at = monotonic()
    overlay = render_global_loading_overlay(
        message,
        hint=hint,
        estimated_seconds=(
            estimated_seconds
            if estimated_seconds is not None
            else min_visible_seconds
            if min_visible_seconds > 0
            else None
        ),
    )

    try:
        yield

    finally:
        remaining_seconds = min_visible_seconds - (monotonic() - started_at)

        if remaining_seconds > 0:
            sleep(remaining_seconds)

        overlay.empty()
