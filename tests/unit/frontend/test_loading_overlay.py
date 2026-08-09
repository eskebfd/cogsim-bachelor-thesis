from frontend.shared.styles.components.loading_overlay import LOADING_OVERLAY_CSS
from frontend.shared.ui import loading_overlay


class FakePlaceholder:
    def __init__(self):
        self.markdown_calls = []
        self.emptied = False

    def markdown(self, body, **kwargs):
        self.markdown_calls.append((body, kwargs))

    def empty(self):
        self.emptied = True


def test_global_loading_overlay_renders_escaped_message(monkeypatch):
    placeholder = FakePlaceholder()
    monkeypatch.setattr(
        loading_overlay.st,
        "empty",
        lambda: placeholder,
    )

    rendered = loading_overlay.render_global_loading_overlay(
        'Szenario <analysieren>'
    )

    assert rendered is placeholder
    assert "cogsim-loading-overlay" in placeholder.markdown_calls[0][0]
    assert "Szenario &lt;analysieren&gt;" in placeholder.markdown_calls[0][0]
    assert "cogsim-loading-overlay__progress" in placeholder.markdown_calls[0][0]
    assert "cogsim-loading-overlay__mascot" in placeholder.markdown_calls[0][0]
    assert "cogsim-pixel-dino" in placeholder.markdown_calls[0][0]
    assert "🦖" not in placeholder.markdown_calls[0][0]
    assert "Geschätzte Dauer" in placeholder.markdown_calls[0][0]
    assert placeholder.markdown_calls[0][1]["unsafe_allow_html"] is True


def test_global_loading_overlay_renders_estimated_duration(monkeypatch):
    placeholder = FakePlaceholder()
    monkeypatch.setattr(
        loading_overlay.st,
        "empty",
        lambda: placeholder,
    )

    loading_overlay.render_global_loading_overlay(
        "Simulation läuft.",
        estimated_seconds=7.0,
    )

    body = placeholder.markdown_calls[0][0]
    assert "etwa 7 Sekunden" in body
    assert (
        '<div class="cogsim-loading-overlay__panel" '
        'style="--cogsim-loading-duration: 7.0s;">'
    ) in body
    assert (
        '<div class="cogsim-loading-overlay__progress" role="progressbar" '
        'aria-label="Geschätzter Fortschritt" >'
    ) in body


def test_global_loading_context_clears_overlay(monkeypatch):
    placeholder = FakePlaceholder()
    monkeypatch.setattr(
        loading_overlay.st,
        "empty",
        lambda: placeholder,
    )

    with loading_overlay.global_loading("Modelle werden erstellt..."):
        assert placeholder.emptied is False

    assert placeholder.emptied is True


def test_stale_loading_overlay_cleanup_is_rendered(monkeypatch):
    rendered_markup = []
    monkeypatch.setattr(
        loading_overlay.st,
        "markdown",
        lambda body, **kwargs: rendered_markup.append((body, kwargs)),
    )

    loading_overlay.clear_stale_global_loading_overlay()

    body, kwargs = rendered_markup[0]
    assert ".cogsim-loading-overlay" in body
    assert "display: none !important" in body
    assert "pointer-events: none !important" in body
    assert kwargs["unsafe_allow_html"] is True


def test_loading_overlay_css_blocks_interaction_and_blurs_background():
    assert "position: fixed" in LOADING_OVERLAY_CSS
    assert "backdrop-filter: blur" in LOADING_OVERLAY_CSS
    assert "pointer-events: auto" in LOADING_OVERLAY_CSS
    assert "cogsim-loading-progress" in LOADING_OVERLAY_CSS
    assert "cogsim-loading-dino-run" in LOADING_OVERLAY_CSS
    assert "cogsim-pixel-dino" in LOADING_OVERLAY_CSS
    assert "cogsim-loading-progress var(--cogsim-loading-duration, 18s)\n                linear forwards" in LOADING_OVERLAY_CSS


def test_global_loading_context_respects_minimum_visible_duration(monkeypatch):
    placeholder = FakePlaceholder()
    sleep_calls = []
    times = iter([10.0, 12.5])

    monkeypatch.setattr(
        loading_overlay.st,
        "empty",
        lambda: placeholder,
    )
    monkeypatch.setattr(
        loading_overlay,
        "monotonic",
        lambda: next(times),
    )
    monkeypatch.setattr(
        loading_overlay,
        "sleep",
        lambda seconds: sleep_calls.append(seconds),
    )

    with loading_overlay.global_loading(
        "Die Simulation läuft.",
        min_visible_seconds=7.0,
    ):
        pass

    assert sleep_calls == [4.5]
    assert placeholder.emptied is True
