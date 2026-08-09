import streamlit as st


def render_info_message(message: str) -> None:
    st.markdown(
        f'<div class="status-message status-info">{message}</div>',
        unsafe_allow_html=True,
    )


def render_warning_message(message: str) -> None:
    st.markdown(
        f'<div class="status-message status-warning">{message}</div>',
        unsafe_allow_html=True,
    )


def render_success_message(message: str) -> None:
    st.markdown(
        f'<div class="status-message status-success">{message}</div>',
        unsafe_allow_html=True,
    )
