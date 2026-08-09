import html

import streamlit as st

DESCRIPTION_KEYS = [
    "beschreibung",
    "description",
    "begründung",
    "reasoning",
]


TITLE_KEYS = [
    "name",
    "label",
    "metric_id",
    "operation_id",
    "subziel_id",
    "plan_id",
]


ATTRIBUTE_VALUE_KEYS = {
    "value",
    "scale_min_description",
    "scale_max_description",
    "explanation",
    "confidence",
}


def is_attribute_value(data: dict) -> bool:
    return ATTRIBUTE_VALUE_KEYS.issubset(data.keys())


def render_box(value) -> None:
    safe_value = html.escape(str(value if value is not None else "Nicht angegeben"))

    st.markdown(
        f'<div class="review-box">{safe_value}</div>',
        unsafe_allow_html=True,
    )


def render_badge_value(value) -> None:
    safe_value = html.escape(str(value if value else "Nicht angegeben"))

    st.markdown(
        f'<span class="review-badge">{safe_value}</span>',
        unsafe_allow_html=True,
    )


def render_attribute_value(data: dict) -> None:
    render_text_value("value", data.get("value"))

    st.caption(
        f"0: {data.get('scale_min_description', 'Nicht angegeben')} · "
        f"100: {data.get('scale_max_description', 'Nicht angegeben')}"
    )

    render_text_value("explanation", data.get("explanation"))
    render_text_value("confidence", data.get("confidence"))


def render_text_value(label: str, value) -> None:
    readable_label = label.replace("_", " ").title()
    normalized_label = label.replace("_", " ").strip().lower()

    st.markdown(
        f'<div class="review-label">{html.escape(readable_label)}</div>',
        unsafe_allow_html=True,
    )

    if isinstance(value, str) and value.lower().strip() in [
        "low",
        "medium",
        "high",
        "positive",
        "neutral",
        "negative",
    ]:
        render_badge_value(value)

        if normalized_label == "confidence":
            st.caption(
                "Confidence beschreibt nur, wie sicher der Attributwert "
                "geschätzt wurde. Sie beeinflusst keine Simulation."
            )
    else:
        render_box(value)


def render_list(items: list, empty_text: str) -> None:
    if not items:
        st.info(empty_text)
        return

    for item in items:
        render_box(item)


def render_feedback_area(label: str, key: str, placeholder: str) -> str:
    return st.text_area(
        label,
        key=key,
        placeholder=placeholder,
        height=90,
    )


def collect_review_feedback(prefix: str) -> dict:
    feedback = {}

    for key, value in st.session_state.items():
        if key.startswith(prefix) and isinstance(value, str) and value.strip():
            clean_key = key.replace(prefix, "")
            feedback[clean_key] = value.strip()

    return feedback


def model_attribute_value(attribute) -> float | str:
    if isinstance(attribute, dict):
        return attribute.get("value", "-")
    return attribute if attribute is not None else "-"


def model_attribute_meaning(attribute) -> str:
    if not isinstance(attribute, dict):
        return ""
    return str(attribute.get("explanation") or attribute.get("description") or "")


def _coerce_model_value(value, fallback: int = 50) -> int:
    try:
        parsed = int(float(value))
    except (TypeError, ValueError):
        parsed = fallback
    return max(0, min(100, parsed))


def value_intensity_label(value: int) -> str:
    if value <= 24:
        return "sehr niedrig"

    if value <= 49:
        return "niedrig bis moderat"

    if value <= 74:
        return "deutlich vorhanden"

    return "stark ausgeprägt"


def build_dynamic_model_attribute_meaning(
    *,
    label: str,
    value: int,
    attribute: dict | int | float | None,
) -> str:
    value = _coerce_model_value(value)
    intensity = value_intensity_label(value)

    if isinstance(attribute, dict):
        min_description = attribute.get("scale_min_description")
        max_description = attribute.get("scale_max_description")
        if min_description and max_description:
            closer_description = (
                max_description if value >= 50 else min_description
            )
            opposite_description = (
                min_description if value >= 50 else max_description
            )
            return (
                f"{label} liegt mit {value} von 100 {intensity} und näher an "
                f"„{closer_description}“ als an „{opposite_description}“."
            )

    return f"{label} liegt mit {value} von 100 im Bereich „{intensity}“."


def build_live_model_attribute_rows(
    model: dict,
    attributes: tuple[tuple[str, str], ...],
    current_values: dict | None = None,
) -> list[dict]:
    current_values = current_values or {}

    rows = []
    for attribute_id, label in attributes:
        if attribute_id not in model:
            continue

        value = current_values.get(
            attribute_id,
            model_attribute_value(model.get(attribute_id)),
        )
        display_value = _coerce_model_value(value)

        rows.append(
            {
                "Attribut": label,
                "Aktueller Wert": display_value,
            }
        )

    return rows


def dataframe_height(row_count: int, *, min_height: int = 140) -> int:
    return max(min_height, 44 + row_count * 35)


def _attribute_help_text(attribute: dict | int | float | None) -> str:
    if not isinstance(attribute, dict):
        return ""

    return str(attribute.get("explanation") or "").strip()


def _render_attribute_value_card(
    *,
    attribute_id: str,
    label: str,
    value: int | str,
    attribute: dict | int | float | None,
) -> None:
    help_text = _attribute_help_text(attribute)
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    safe_help = html.escape(help_text)
    numeric_value = _coerce_model_value(value)

    with st.container(key=f"attribute_value_card_{attribute_id}"):
        description = (
            '<div class="cogsim-attribute-value-card__description">'
            f"{safe_help}"
            "</div>"
            if safe_help
            else ""
        )
        st.markdown(
            (
                '<div class="cogsim-attribute-value-card__content">'
                '<div class="cogsim-attribute-value-card__main">'
                '<div class="cogsim-attribute-value-card__label">'
                f"{safe_label}"
                "</div>"
                f"{description}"
                "</div>"
                '<div class="cogsim-attribute-value-card__value">'
                f"{safe_value}"
                "</div>"
                "</div>"
                '<div class="cogsim-attribute-value-card__scale">'
                '<div class="cogsim-attribute-value-card__track">'
                f'<span style="width:{numeric_value}%"></span>'
                "</div>"
                '<div class="cogsim-attribute-value-card__scale-labels">'
                "<span>0</span>"
                "<span>100</span>"
                "</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )


def render_model_attribute_summary(
    *,
    title: str,
    help_text: str,
    model: dict,
    attributes: tuple[tuple[str, str], ...],
    current_values: dict | None = None,
    edit_action=None,
) -> list[dict]:
    rows = build_live_model_attribute_rows(
        model,
        attributes,
        current_values,
    )

    if edit_action is not None:
        with st.container(
            key=f"model_attribute_edit_action_{title.lower().replace(' ', '_')}",
        ):
            _, action_column = st.columns([0.88, 0.12])
            with action_column:
                edit_action()

    with st.container(
        key=f"model_attribute_summary_{title.lower().replace(' ', '_')}",
    ):
        row_by_attribute = {
            attribute_id: row
            for attribute_id, label in attributes
            for row in rows
            if row.get("Attribut") == label
        }

        for left_index in range(0, len(attributes), 2):
            columns = st.columns(
                2,
                gap="small",
            )
            for column, (attribute_id, label) in zip(
                columns,
                attributes[left_index : left_index + 2],
            ):
                row = row_by_attribute.get(attribute_id)
                if not row:
                    continue
                with column:
                    _render_attribute_value_card(
                        attribute_id=attribute_id,
                        label=label,
                        value=row["Aktueller Wert"],
                        attribute=model.get(attribute_id),
                    )

        st.markdown(
            '<div class="cogsim-attribute-value-grid-spacer"></div>',
            unsafe_allow_html=True,
        )

    return rows


def get_card_title(item: dict, fallback_title: str, index: int) -> str:
    for key in TITLE_KEYS:
        if item.get(key):
            return str(item.get(key))

    return f"{fallback_title} {index + 1}"


def get_primary_description(item: dict):
    for key in DESCRIPTION_KEYS:
        if item.get(key):
            return item.get(key)

    return None


def render_primary_description(item: dict) -> None:
    description = get_primary_description(item)

    if description:
        render_box(description)


def render_section_title(title: str) -> None:
    st.markdown(
        f'<div class="review-section-title">{html.escape(title)}</div>',
        unsafe_allow_html=True,
    )


def render_dict_details(data: dict, parent_key: str = "details") -> None:
    if is_attribute_value(data):
        render_attribute_value(data)
        return

    render_primary_description(data)

    for key, value in data.items():
        if key in DESCRIPTION_KEYS:
            continue

        readable_key = key.replace("_", " ").title()

        if isinstance(value, list):
            render_section_title(readable_key)

            if value and all(isinstance(item, dict) for item in value):
                render_schema_cards(
                    value,
                    key_prefix=f"review_nested_{parent_key}_{key}",
                    feedback_label=f"Feedback zu {readable_key}",
                    fallback_title=readable_key,
                    show_feedback=False,
                )
            else:
                render_list(value, "Keine Einträge vorhanden.")

        elif isinstance(value, dict):
            with st.expander(readable_key, expanded=False):
                render_dict_details(value, parent_key=f"{parent_key}_{key}")

        else:
            render_text_value(readable_key, value)


def render_schema_card_content(
    item: dict,
    index: int,
    key_prefix: str,
) -> None:
    render_primary_description(item)

    for key, value in item.items():
        if key in TITLE_KEYS or key in DESCRIPTION_KEYS:
            continue

        readable_key = key.replace("_", " ").title()

        if isinstance(value, list):
            render_section_title(readable_key)

            if value and all(isinstance(nested, dict) for nested in value):
                render_schema_cards(
                    value,
                    key_prefix=f"{key_prefix}_{index}_{key}",
                    feedback_label=f"Feedback zu {readable_key}",
                    fallback_title=readable_key,
                    show_feedback=False,
                )
            else:
                render_list(value, "Keine Einträge vorhanden.")

        elif isinstance(value, dict):
            with st.expander(readable_key, expanded=False):
                render_dict_details(
                    value,
                    parent_key=f"{key_prefix}_{index}_{key}",
                )

        else:
            render_text_value(readable_key, value)


def render_schema_cards(
    items: list,
    key_prefix: str,
    feedback_label: str,
    fallback_title: str = "Eintrag",
    show_feedback: bool = True,
) -> None:
    if not items:
        st.info("Keine Einträge vorhanden.")
        return

    for index, item in enumerate(items):
        if isinstance(item, dict):
            title = get_card_title(item, fallback_title, index)

            with st.expander(title, expanded=False):
                render_schema_card_content(
                    item=item,
                    index=index,
                    key_prefix=key_prefix,
                )

                if show_feedback:
                    render_feedback_area(
                        feedback_label,
                        key=f"{key_prefix}_{index}",
                        placeholder="Was soll an diesem Eintrag geändert werden?",
                    )

        else:
            with st.expander(f"{fallback_title} {index + 1}", expanded=False):
                render_box(item)

                if show_feedback:
                    render_feedback_area(
                        feedback_label,
                        key=f"{key_prefix}_{index}",
                        placeholder="Was soll an diesem Eintrag geändert werden?",
                    )
