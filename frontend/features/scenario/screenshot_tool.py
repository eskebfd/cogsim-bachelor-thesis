import base64
from html import escape

import streamlit as st

from backend.domains.scenario.services.image_processing import (
    ALLOWED_SCENARIO_IMAGE_MIME_TYPES,
    MAX_SCENARIO_IMAGE_BYTES,
)
from frontend.shared.services.workflow_api import (
    analyze_screenshot_task_structure,
)
from frontend.shared.ui.icons import render_icon
from frontend.shared.ui.loading_overlay import global_loading
from frontend.state import (
    DEFAULT_SCENARIO_INTERFACE,
    DEFAULT_SCENARIO_TASK,
    get_session_id,
)


def build_scenario_image_payload(uploaded_file) -> dict | None:
    if uploaded_file is None:
        return None

    if uploaded_file.type not in ALLOWED_SCENARIO_IMAGE_MIME_TYPES:
        st.error("Ungültiges Dateiformat. "  "Erlaubt sind PNG, JPG, JPEG und WEBP.")
        return None

    image_bytes = uploaded_file.getvalue()

    if not image_bytes:
        st.error("Die hochgeladene Datei ist leer.")
        return None

    if len(image_bytes) > MAX_SCENARIO_IMAGE_BYTES:
        max_size_mb = MAX_SCENARIO_IMAGE_BYTES // (1024 * 1024)

        st.error(f"Das Bild ist zu groß. "  f"Maximal erlaubt sind {max_size_mb} MB.")
        return None

    return {
        "filename": uploaded_file.name,
        "mime_type": uploaded_file.type,
        "size_bytes": len(image_bytes),
        "data_base64": base64.b64encode(image_bytes).decode("ascii"),
    }


def _format_file_size(size_bytes: int) -> str:
    size_kb = size_bytes / 1024

    if size_kb < 1024:
        return f"{size_kb:.0f} KB"

    return f"{size_kb / 1024:.1f} MB"


def build_screenshot_analysis_image_key(
    payload: dict | None,
) -> tuple | None:
    if not payload:
        return None

    data_base64 = payload.get("data_base64", "")

    return (
        payload.get("filename"),
        payload.get("mime_type"),
        payload.get("size_bytes"),
        data_base64[:32],
        data_base64[-32:],
    )


def reset_screenshot_analysis_state() -> None:
    st.session_state.screenshot_task_analysis = None
    st.session_state.screenshot_task_analysis_error = None
    st.session_state.screenshot_task_analysis_image_key = None
    st.session_state.screenshot_task_analysis_applied_key = None
    st.session_state.screenshot_task_analysis_pending_text = None
    st.session_state.screenshot_interface_analysis_pending_text = None


def _render_section_header(
    icon: str,
    title: str,
    description: str,
) -> None:
    header_html = (
        '<div class="cogsim-scenario-section-header">'
        '<div class="cogsim-scenario-section-icon">'
        f"{render_icon(icon, size=20, stroke_width=1.8)}"
        "</div>"
        '<div class="cogsim-scenario-section-copy">'
        f'<div class="cogsim-scenario-section-title">{title}</div>'
        '<div class="cogsim-scenario-section-description">'
        f"{description}"
        "</div>"
        "</div>"
        "</div>"
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True,
    )


def _remove_uploaded_image() -> None:
    st.session_state.scenario_image_upload = None

    st.session_state.scenario_image_uploader_version = (
        st.session_state.get(
            "scenario_image_uploader_version",
            0,
        )
        + 1
    )

    reset_screenshot_analysis_state()


def _format_screenshot_analysis_for_task_field(analysis: dict | None) -> str:
    if not analysis:
        return ""

    task_description = str(analysis.get("task_description") or "").strip()
    user_goal = str(analysis.get("user_goal") or "").strip()
    main_task = str(analysis.get("main_task") or "").strip()
    hta_steps = analysis.get("hta_steps") or []

    if task_description:
        lines = [
            "Aus dem Screenshot abgeleiteter Aufgabenablauf",
            "",
            task_description,
        ]
    else:
        lines = ["Aus dem Screenshot abgeleiteter Aufgabenablauf"]

    if user_goal and not task_description:
        lines.extend(["", f"Ziel: {user_goal}"])

    if main_task and not task_description:
        lines.extend(["", f"Hauptaufgabe: {main_task}"])

    step_lines = []

    for index, step in enumerate(hta_steps, start=1):
        if not isinstance(step, dict):
            continue

        number = str(step.get("number") or index).strip()
        title = str(step.get("title") or "").strip()
        description = str(step.get("description") or "").strip()

        if not title and not description:
            continue

        step_line = f"{number}. {title}" if title else f"{number}. {description}"

        if title and description:
            step_line = f"{step_line} – {description}"

        step_lines.append(step_line)

    if step_lines:
        lines.extend(["", "Mögliche Arbeitsschritte:"])
        lines.extend(step_lines)

    lines.extend(
        [
            "",
            "Hinweis: Die Schritte sind plausible Hypothesen aus dem Screenshot.",
        ]
    )

    return "\n".join(lines)


def _format_screenshot_analysis_for_interface_field(analysis: dict | None) -> str:
    if not analysis:
        return ""

    interface_description = str(
        analysis.get("interface_description") or ""
    ).strip()
    elements = analysis.get("visible_elements") or analysis.get("interface_elements") or []
    uncertainties = analysis.get("uncertainties") or analysis.get("missing_information") or []

    lines = []
    if interface_description:
        lines.extend(["Aus dem Screenshot erkannte Interface-Hinweise", "", interface_description])

    visible_elements = [
        str(element).strip()
        for element in elements
        if str(element).strip()
    ]
    if visible_elements:
        lines.extend(
            [
                "",
                "Sichtbare Elemente:",
                ", ".join(visible_elements[:8]) + ".",
            ]
        )

    clear_uncertainties = [
        str(item).strip()
        for item in uncertainties
        if str(item).strip()
    ]
    if clear_uncertainties:
        lines.extend(
            [
                "",
                "Unsicher aus dem Screenshot:",
                "; ".join(clear_uncertainties[:3]) + ".",
            ]
        )

    return "\n".join(lines).strip()


def _field_can_be_replaced(current_value: str, default_value: str) -> bool:
    current = str(current_value or "").strip()
    return not current or current == default_value.strip()


def _apply_screenshot_analysis_to_scenario_fields(
    analysis: dict | None,
    image_key: tuple | None,
) -> None:
    generated_task_text = _format_screenshot_analysis_for_task_field(analysis)
    generated_interface_text = _format_screenshot_analysis_for_interface_field(analysis)

    if not image_key:
        return

    if st.session_state.get("screenshot_task_analysis_applied_key") == image_key:
        return

    current_task = str(st.session_state.get("scenario_task", "") or "").strip()
    current_interface = str(
        st.session_state.get("scenario_interface", "") or ""
    ).strip()

    if generated_task_text and _field_can_be_replaced(
        current_task,
        DEFAULT_SCENARIO_TASK,
    ):
        st.session_state.screenshot_task_analysis_pending_text = generated_task_text

    if generated_interface_text and _field_can_be_replaced(
        current_interface,
        DEFAULT_SCENARIO_INTERFACE,
    ):
        st.session_state.screenshot_interface_analysis_pending_text = (
            generated_interface_text
        )

    st.session_state.screenshot_task_analysis_applied_key = image_key


def _apply_screenshot_analysis_to_task_field(
    analysis: dict | None,
    image_key: tuple | None,
) -> None:
    _apply_screenshot_analysis_to_scenario_fields(analysis, image_key)


def apply_pending_screenshot_task_text() -> None:
    pending_text = st.session_state.get("screenshot_task_analysis_pending_text")
    pending_interface_text = st.session_state.get(
        "screenshot_interface_analysis_pending_text"
    )

    if pending_text:
        st.session_state.scenario_task = pending_text
        st.session_state.screenshot_task_analysis_pending_text = None

    if pending_interface_text:
        st.session_state.scenario_interface = pending_interface_text
        st.session_state.screenshot_interface_analysis_pending_text = None


def _render_uploaded_image_card(payload: dict) -> None:
    filename = payload["filename"]
    file_size = _format_file_size(payload["size_bytes"])
    image_src = (
        f"data:{escape(payload['mime_type'])};base64,"
        f"{escape(payload['data_base64'])}"
    )

    with st.container(
        key="uploaded_image_card",
    ):
        preview_column, meta_column, remove_column = st.columns(
            [1.1, 3.4, 0.45],
            gap="small",
            vertical_alignment="center",
        )

        with preview_column:
            st.markdown(
                (
                    '<div class="cogsim-uploaded-image__thumbnail">'
                    f'<img src="{image_src}" alt="{escape(filename)}" />'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

        with meta_column:
            st.markdown(
                (
                    '<div class="cogsim-uploaded-image__meta">'
                    '<div class="cogsim-uploaded-image__status">'
                    "Screenshot hinzugefügt"
                    "</div>"
                    '<div class="cogsim-uploaded-image__title">'
                    f"{escape(filename)}"
                    "</div>"
                    '<div class="cogsim-uploaded-image__footer">'
                    f"{file_size} · Entferne den Screenshot, um ihn zu ersetzen."
                    "</div>"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

        with remove_column:
            st.button(
                "×",
                key="remove_scenario_image_icon",
                help="Bild entfernen",
                on_click=_remove_uploaded_image,
            )


def _analyze_uploaded_screenshot(payload: dict) -> None:
    st.session_state.screenshot_task_analysis_error = None
    image_key = build_screenshot_analysis_image_key(payload)

    with global_loading(
        "Screenshot wird auf erkannte Hinweise analysiert.",
        hint="Aus dem Bild werden sichtbare Arbeitsschritte und Interface-Hinweise erkannt.",
        estimated_seconds=30.0,
    ):
        try:
            response = analyze_screenshot_task_structure(
                payload,
                session_id=get_session_id(),
            )

            st.session_state.screenshot_task_analysis = response.get(
                "screenshot_task_analysis"
            )

            st.session_state.screenshot_task_analysis_image_key = image_key
            _apply_screenshot_analysis_to_scenario_fields(
                st.session_state.screenshot_task_analysis,
                image_key,
            )

        except Exception as exc:
            st.session_state.screenshot_task_analysis = None
            st.session_state.screenshot_task_analysis_error = str(exc)
            st.session_state.screenshot_task_analysis_image_key = image_key


def _render_screenshot_analysis_error() -> None:
    error = st.session_state.get("screenshot_task_analysis_error")

    if error:
        st.error("Screenshot konnte nicht analysiert werden: "  f"{error}")


def _render_screenshot_upload(*, show_header: bool = True) -> None:
    if show_header:
        _render_section_header(
            icon="image",
            title="Screenshot hinzufügen",
            description=("Ergänze optional ein Bild der Website "  "oder Anwendung."),
        )

    existing_payload = st.session_state.get("scenario_image_upload")

    if existing_payload:
        _render_uploaded_image_card(existing_payload)
        _render_screenshot_analysis_error()
        return

    uploader_version = st.session_state.get(
        "scenario_image_uploader_version",
        0,
    )

    uploaded_image = st.file_uploader(
        "Screenshot oder Interface-Bild",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        key=("scenario_image_file_uploader_"  f"{uploader_version}"),
        label_visibility="collapsed",
        help=(
            "PNG, JPG, JPEG oder WEBP. "
            "Keine vertraulichen oder personenbezogenen Daten."
        ),
    )

    if uploaded_image is None:
        return

    payload = build_scenario_image_payload(uploaded_image)

    if payload is None:
        return

    image_key = build_screenshot_analysis_image_key(payload)

    if st.session_state.get("screenshot_task_analysis_image_key") != image_key:
        reset_screenshot_analysis_state()

    st.session_state.scenario_image_upload = payload

    _analyze_uploaded_screenshot(payload)

    if hasattr(st, "rerun"):
        st.rerun()

    _render_uploaded_image_card(payload)
    _render_screenshot_analysis_error()


def _render_task_screenshot_attachment() -> None:
    with st.container(key="scenario_task_screenshot_attachment"):
        st.markdown(
            (
                '<div class="cogsim-task-screenshot-callout">'
                '<div class="cogsim-task-screenshot-callout__icon">'
                f"{render_icon('image', size=18, stroke_width=1.9)}"
                "</div>"
                '<div class="cogsim-task-screenshot-callout__copy">'
                '<div class="cogsim-task-screenshot-callout__title">'
                "Aufgabe mit Screenshot ergänzen"
                "</div>"
                '<div class="cogsim-task-screenshot-callout__text">'
                "Optional kannst du ein Bild der Oberfläche hochladen. CogSim "
                "trennt daraus sichtbare Arbeitsschritte und Interface-Hinweise."
                "</div>"
                "</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        _render_screenshot_upload(show_header=False)
