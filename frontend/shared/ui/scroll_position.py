import streamlit as st
import streamlit.components.v1 as components


def render_scroll_to_top_on_page_change(page_key: str) -> None:
    if st.session_state.get("_last_scroll_page_key") == page_key:
        return

    st.session_state["_last_scroll_page_key"] = page_key

    components.html(
        """
        <script>
            const scrollTop = () => {
                const doc = window.parent.document;
                window.parent.scrollTo({ top: 0, left: 0, behavior: "auto" });
                doc.documentElement.scrollTop = 0;
                doc.body.scrollTop = 0;
                const main = doc.querySelector('[data-testid="stMain"]');
                if (main) {
                    main.scrollTop = 0;
                }
            };
            scrollTop();
            window.parent.requestAnimationFrame(scrollTop);
            window.parent.setTimeout(scrollTop, 80);
        </script>
        """,
        height=0,
        width=0,
    )
