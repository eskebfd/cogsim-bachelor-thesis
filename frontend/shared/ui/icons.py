from html import escape

_ICONS = {
    "user": (
        '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/>'
    ),
    "users": (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>'
        '<circle cx="9" cy="7" r="4"/>'
        '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
    ),
    "home": (
        '<path d="M3 10.5 12 3l9 7.5"/>'
        '<path d="M5 9.5V21h14V9.5"/>'
        '<path d="M9 21v-6h6v6"/>'
    ),
    "file-text": (
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/>'
        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
        '<path d="M10 9H8"/>'
        '<path d="M16 13H8"/>'
        '<path d="M16 17H8"/>'
    ),
    "image": (
        '<rect x="3" y="3" width="18" height="18" rx="2"/>'
        '<circle cx="8.5" cy="8.5" r="1.5"/>'
        '<path d="m21 15-5-5L5 21"/>'
    ),
    "sliders-horizontal": (
        '<path d="M21 4h-7"/>'
        '<path d="M10 4H3"/>'
        '<path d="M21 12h-9"/>'
        '<path d="M8 12H3"/>'
        '<path d="M21 20h-5"/>'
        '<path d="M12 20H3"/>'
        '<circle cx="12" cy="4" r="2"/>'
        '<circle cx="10" cy="12" r="2"/>'
        '<circle cx="14" cy="20" r="2"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "boxes": (
        '<path d="M2.97 12.92 12 17.99l9.03-5.07"/>'
        '<path d="M2.97 7.08 12 12.15l9.03-5.07L12 2z"/>'
        '<path d="M12 22.02v-4.03"/>'
        '<path d="M7.5 15.46v-4.04"/>'
        '<path d="M16.5 15.46v-4.04"/>'
    ),
    "calculator": (
        '<rect width="16" height="20" x="4" y="2" rx="2"/>'
        '<line x1="8" x2="16" y1="6" y2="6"/>'
        '<line x1="16" x2="16" y1="14" y2="18"/>'
        '<path d="M8 10h.01"/>'
        '<path d="M12 10h.01"/>'
        '<path d="M16 10h.01"/>'
        '<path d="M8 14h.01"/>'
        '<path d="M12 14h.01"/>'
        '<path d="M8 18h.01"/>'
        '<path d="M12 18h.01"/>'
    ),
    "play-circle": (
        '<circle cx="12" cy="12" r="10"/>'  '<polygon points="10 8 16 12 10 16 10 8"/>'
    ),
    "bar-chart-3": (
        '<path d="M3 3v18h18"/>'
        '<path d="M18 17V9"/>'
        '<path d="M13 17V5"/>'
        '<path d="M8 17v-3"/>'
    ),
    "check": ('<path d="M20 6 9 17l-5-5"/>'),
    "circle": ('<circle cx="12" cy="12" r="10"/>'),
    "brain": (
        '<path d="M12 5a3 3 0 1 0-5.99.2A3 3 0 0 0 4 8a3 3 0 0 0 2 2.83"/>'
        '<path d="M12 5a3 3 0 1 1 5.99.2A3 3 0 0 1 20 8a3 3 0 0 1-2 2.83"/>'
        '<path d="M12 5v14"/>'
        '<path d="M6 10v4a4 4 0 0 0 4 4"/>'
        '<path d="M18 10v4a4 4 0 0 1-4 4"/>'
    ),
    "book-open": (
        '<path d="M2 4h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 4h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "shield": ('<path d="M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V5l8-3 8 3z"/>'),
    "shield-alert": (
        '<path d="M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V5l8-3 8 3z"/>'
        '<path d="M12 8v4"/>'
        '<path d="M12 16h.01"/>'
    ),
    "gauge": (
        '<path d="m12 14 4-4"/>'
        '<path d="M3.34 19a10 10 0 1 1 17.32 0"/>'
        '<path d="M12 19a2 2 0 0 0 2-2c0-1.1-.9-2-2-2s-2 .9-2 2a2 2 0 0 0 2 2z"/>'
    ),
    "check-circle-2": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "timer": (
        '<line x1="10" x2="14" y1="2" y2="2"/>'
        '<line x1="12" x2="15" y1="14" y2="11"/>'
        '<circle cx="12" cy="14" r="8"/>'
    ),
    "clock-alert": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M12 6v6l4 2"/>'
        '<path d="M12 18h.01"/>'
    ),
    "book-open-text": (
        '<path d="M2 4h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 4h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
        '<path d="M6 8h2"/>'
        '<path d="M6 12h2"/>'
        '<path d="M16 8h2"/>'
        '<path d="M16 12h2"/>'
    ),
    "activity": (
        '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'
    ),
}


def lucide_icon(
    name: str,
    *,
    size: int = 20,
    stroke_width: float = 2,
    color: str = "currentColor",
    label: str = "",
) -> str:
    body = _ICONS.get(name, _ICONS["circle"])
    aria = f'aria-label="{escape(label)}"' if label else 'aria-hidden="true"'

    return (
        f'<span class="cogsim-icon" {aria}>'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" '
        f'height="{size}" '
        f'viewBox="0 0 24 24" '
        f'fill="none" '
        f'stroke="{color}" '
        f'stroke-width="{stroke_width}" '
        f'stroke-linecap="round" '
        f'stroke-linejoin="round">'
        f"{body}"
        f"</svg>"
        f"</span>"
    )


render_icon = lucide_icon
