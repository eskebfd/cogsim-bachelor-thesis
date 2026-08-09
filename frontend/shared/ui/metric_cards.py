from html import escape

import streamlit as st


def _value_kind(value: object) -> str:
    text = str(value).strip()

    if not text:
        return "text"

    numeric_text = (
        text.replace(",", ".")
        .replace("%", "")
        .replace("s", "")
        .replace(" ", "")
    )

    try:
        float(numeric_text)
    except ValueError:
        return "text"

    return "numeric"


def render_metric_card(
    label: str,
    value: object,
    caption: str = "",
    *,
    value_kind: str | None = None,
) -> None:
    kind = value_kind or _value_kind(value)

    st.markdown(
        f"""
        <div class="cogsim-kpi-card">
            <div class="cogsim-kpi-label">{escape(label)}</div>
            <div class="cogsim-kpi-value cogsim-kpi-value--{escape(kind)}">
                {escape(str(value))}
            </div>
            <div class="cogsim-kpi-caption">{escape(caption)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
