from html import escape
from copy import deepcopy

import streamlit as st

from frontend.features.models.common import (
    build_live_model_attribute_rows,
    render_model_attribute_summary,
)
from frontend.shared.model_attribute_labels import (
    TASK_ATTRIBUTE_LABELS,
    attribute_items,
)

TASK_EDITABLE_ATTRIBUTES = attribute_items(TASK_ATTRIBUTE_LABELS)

GOMS_OPERATION_LABELS = {
    "perceive": "wahrnehmen",
    "think": "nachdenken",
    "point": "zum Element bewegen",
    "click": "klicken",
    "type": "eingeben",
    "read": "lesen",
    "verify": "prüfen",
    "wait": "warten",
    "submit": "abschicken",
    "select": "auswählen",
    "input": "eingeben",
    "navigate": "zur nächsten Stelle wechseln",
    "check": "kontrollieren",
    "compare": "vergleichen",
    "scroll": "scrollen",
    "search": "suchen",
}


def _translate_goms_operation(operation: str | None) -> str:
    if not operation:
        return "-"

    normalized = str(operation).strip().lower()
    return GOMS_OPERATION_LABELS.get(
        normalized,
        normalized.replace("_", " "),
    )


def _format_goms_operations(
    step: dict,
) -> str:
    estimates = step.get(
        "operation_time_estimates",
        [],
    )

    if estimates:
        return ", ".join(
            (
                f"{_translate_goms_operation(item.get('operation'))}"
                f" ({item.get('estimated_duration_seconds', 0):g} s)"
            )
            for item in estimates
        )

    return ", ".join(
        _translate_goms_operation(operation)
        for operation in step.get(
            "goms_operations",
            [],
        )
    )


def build_task_step_rows(
    task_model: dict,
) -> list[dict]:
    rows = []

    for index, step in enumerate(
        task_model.get("steps", []),
        start=1,
    ):
        rows.append(
            {
                "Schritt": index,
                "HTA-Schritt": step.get(
                    "name",
                    "",
                ),
                "Beschreibung": step.get(
                    "description",
                    "",
                ),
                "GOMS-Operationen": _format_goms_operations(step),
                "Dauer": (f"{step.get('estimated_duration_seconds', 0):g} s"),
                "Kognitive Anforderungen": ", ".join(
                    step.get(
                        "cognitive_requirements",
                        [],
                    )
                ),
            }
        )

    return rows


def _duration_value(step: dict) -> float:
    try:
        return float(step.get("estimated_duration_seconds") or 0)
    except (TypeError, ValueError):
        return 0.0


def _renumber_steps(steps: list[dict]) -> list[dict]:
    updated_steps = []
    for index, step in enumerate(steps, start=1):
        updated_step = {
            **step,
            "step_order": index,
            "sequence_order": index,
        }
        if not updated_step.get("step_id"):
            updated_step["step_id"] = f"step_{index}"
        updated_steps.append(updated_step)
    return updated_steps


def _update_task_model_steps(steps: list[dict]) -> None:
    base_model_preview = deepcopy(st.session_state.get("base_model_preview") or {})
    backend_state = deepcopy(st.session_state.get("backend_state") or {})
    task_model = deepcopy(
        base_model_preview.get("task_model")
        or backend_state.get("task_model")
        or {}
    )
    task_model["steps"] = _renumber_steps(steps)
    base_model_preview["task_model"] = task_model
    backend_state["task_model"] = task_model
    st.session_state.base_model_preview = base_model_preview
    st.session_state.backend_state = backend_state
    st.session_state.computed_parameters_preview = None
    st.session_state.simulation_plan_review = None
    st.session_state.simulation_result = None


def _scaled_operation_estimates(
    estimates: list[dict],
    old_duration: float,
    new_duration: float,
) -> list[dict]:
    if not estimates:
        return estimates
    if old_duration <= 0:
        return [
            {
                **estimate,
                "estimated_duration_seconds": round(
                    new_duration / max(1, len(estimates)),
                    2,
                ),
            }
            for estimate in estimates
        ]
    factor = new_duration / old_duration
    return [
        {
            **estimate,
            "estimated_duration_seconds": round(
                float(estimate.get("estimated_duration_seconds") or 0) * factor,
                2,
            ),
        }
        for estimate in estimates
    ]


def _render_task_step_editor(
    *,
    task_model: dict,
    step: dict,
    index: int,
) -> None:
    with st.expander(
        f"Schritt {index} bearbeiten",
        expanded=False,
    ):
        with st.form(
            f"task_step_edit_form_{index}",
            clear_on_submit=False,
        ):
            edited_name = st.text_input(
                "Name des Schritts",
                value=str(step.get("name") or ""),
                key=f"task_step_name_{index}",
            )
            edited_description = st.text_area(
                "Beschreibung",
                value=str(step.get("description") or ""),
                height=86,
                key=f"task_step_description_{index}",
            )
            edited_duration = st.number_input(
                "Geschätzte Dauer in Sekunden",
                min_value=1.0,
                max_value=300.0,
                value=max(1.0, _duration_value(step)),
                step=1.0,
                key=f"task_step_duration_{index}",
            )
            submit_update = st.form_submit_button(
                "Änderungen übernehmen",
                type="secondary",
                use_container_width=True,
            )

        delete_step = st.button(
            "Schritt entfernen",
            key=f"task_step_delete_{index}",
            type="secondary",
            use_container_width=True,
            disabled=len(task_model.get("steps", [])) <= 1,
        )

        steps = deepcopy(task_model.get("steps", []))
        if submit_update and 0 <= index - 1 < len(steps):
            old_step = steps[index - 1]
            old_duration = _duration_value(old_step)
            new_duration = float(edited_duration)
            steps[index - 1] = {
                **old_step,
                "name": edited_name.strip() or old_step.get("name") or f"Schritt {index}",
                "description": edited_description.strip(),
                "estimated_duration_seconds": new_duration,
                "duration_seconds": new_duration,
                "operation_time_estimates": _scaled_operation_estimates(
                    old_step.get("operation_time_estimates") or [],
                    old_duration,
                    new_duration,
                ),
            }
            _update_task_model_steps(steps)
            st.rerun()

        if delete_step and 0 <= index - 1 < len(steps):
            del steps[index - 1]
            _update_task_model_steps(steps)
            st.rerun()


def build_task_attribute_rows(
    task_model: dict,
    current_values: dict,
) -> list[dict]:
    return build_live_model_attribute_rows(
        task_model,
        TASK_EDITABLE_ATTRIBUTES,
        current_values,
    )


def _render_missing_step_input() -> str | None:
    with st.container(
        key="missing_task_step",
    ):
        if st.session_state.get("clear_missing_task_step_description"):
            st.session_state.missing_task_step_description = ""
            st.session_state.clear_missing_task_step_description = False

        st.markdown(
            (
                '<div class="cogsim-missing-step-header">'
                '<div class="cogsim-model-subsection-title">'
                "Fehlenden Schritt ergänzen"
                "</div>"
                '<div class="cogsim-model-subsection-copy">'
                "Beschreibe kurz, welcher Arbeitsschritt noch fehlt. "
                "CogSim ergänzt daraus einen passenden Schritt mit "
                "geschätzter Dauer und Anforderungen."
                "</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        with st.form(
            "missing_task_step_form",
            clear_on_submit=False,
        ):
            input_column, button_column = st.columns(
                [11, 1],
                gap="small",
                vertical_alignment="bottom",
            )

            with input_column:
                missing_step_description = st.text_input(
                    "Fehlenden Arbeitsschritt beschreiben",
                    key="missing_task_step_description",
                    placeholder=(
                        "Zum Beispiel: Nach der Suche wählt die Person "
                        "Filter für Preis, Bewertung und Ausstattung aus."
                    ),
                    label_visibility="collapsed",
                )

            with button_column:
                add_step_clicked = st.form_submit_button(
                    "+",
                    type="secondary",
                    use_container_width=True,
                    help="Schritt ergänzen",
                )

        if add_step_clicked:
            return missing_step_description.strip()

    return None


def _render_task_structure(
    task_model: dict,
) -> str | None:
    rows = build_task_step_rows(task_model)

    with st.container(
        key="task_structure_review",
    ):
        st.markdown(
            (
                '<div class="cogsim-model-subsection-title">'
                "Ablauf der Aufgabe"
                "</div>"
                '<div class="cogsim-model-subsection-copy">'
                "Der Zeitstrahl zeigt die erkannten Arbeitsschritte "
                "mit geschätzter Dauer, wichtigen Handlungen und "
                "gedanklicher Belastung."
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        if rows:
            st.markdown(
                '<div class="cogsim-hta-timeline">',
                unsafe_allow_html=True,
            )
            for row, step in zip(rows, task_model.get("steps", [])):
                st.markdown(
                    (
                        '<div class="cogsim-hta-step">'
                            '<div class="cogsim-hta-step__marker">'
                                f"{row['Schritt']}"
                            "</div>"
                            '<div class="cogsim-hta-step__content">'
                                '<div class="cogsim-hta-step__topline">'
                                    '<div class="cogsim-hta-step__title">'
                                        f"{escape(str(row['HTA-Schritt']))}"
                                    "</div>"
                                    '<div class="cogsim-hta-step__duration">'
                                        f"{escape(str(row['Dauer']))}"
                                    "</div>"
                                "</div>"
                                '<div class="cogsim-hta-step__description">'
                                    f"{escape(str(row['Beschreibung'] or 'Keine Beschreibung vorhanden.'))}"
                                "</div>"
                                '<div class="cogsim-hta-step__meta-grid">'
                                    '<div class="cogsim-hta-step__meta">'
                                        '<span class="cogsim-hta-step__meta-label">'
                                            "Handlungen"
                                        "</span>"
                                        '<span class="cogsim-hta-step__meta-value">'
                                            f"{escape(str(row['GOMS-Operationen'] or '-'))}"
                                        "</span>"
                                    "</div>"
                                    '<div class="cogsim-hta-step__meta">'
                                        '<span class="cogsim-hta-step__meta-label">'
                                            "Gedankliche Anforderungen"
                                        "</span>"
                                        '<span class="cogsim-hta-step__meta-value">'
                                            f"{escape(str(row['Kognitive Anforderungen'] or '-'))}"
                                        "</span>"
                                    "</div>"
                                "</div>"
                            "</div>"
                        "</div>"
                    ),
                    unsafe_allow_html=True,
                )
                _render_task_step_editor(
                    task_model=task_model,
                    step=step,
                    index=int(row["Schritt"]),
                )
            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.info("Es wurden noch keine Arbeitsschritte erkannt.")

        return _render_missing_step_input()


def render_task_structure_review(
    task_model: dict,
) -> dict:
    if not task_model:
        st.warning("Kein Aufgabenmodell vorhanden.")
        return {}

    missing_step_request = _render_task_structure(task_model)

    return {
        "missing_step_request": missing_step_request,
    }


def render_task_attribute_review(
    task_model: dict,
    edit_action=None,
) -> dict:
    if not task_model:
        st.warning("Kein Aufgabenmodell vorhanden.")
        return {}

    header_markup = (
        '<div class="cogsim-model-section-header">'
        '<div class="cogsim-model-section-title">'
        "Aufgabenwerte"
        "</div>"
        '<div class="cogsim-model-section-description">'
        "Diese Werte fassen zusammen, wie anspruchsvoll die Aufgabe "
        "für die spätere Simulation eingeschätzt wird."
        "</div>"
        "</div>"
    )
    if edit_action is not None:
        header_column, action_column = st.columns(
            [0.94, 0.06],
            vertical_alignment="top",
        )
        with header_column:
            st.markdown(header_markup, unsafe_allow_html=True)
        with action_column:
            edit_action()
    else:
        st.markdown(header_markup, unsafe_allow_html=True)

    render_model_attribute_summary(
        title="Aktuelle Attributwerte",
        help_text=(
            "Diese Werte fassen zusammen, wie anspruchsvoll die Aufgabe "
            "für die spätere Simulation eingeschätzt wird."
        ),
        model=task_model,
        attributes=TASK_EDITABLE_ATTRIBUTES,
    )

    return {
        "missing_step_request": None,
    }


def render_task_model_review(
    task_model: dict,
    edit_action=None,
) -> dict:
    task_review = render_task_structure_review(task_model)
    render_task_attribute_review(task_model, edit_action=edit_action)
    return task_review
