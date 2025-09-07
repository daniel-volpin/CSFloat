from typing import Optional

import streamlit as st


def render_header(title: str, subtitle: Optional[str] = None) -> None:
    """
    Render the main header for the app with title and optional subtitle.

    Args:
        title (str): The main title to display.
        subtitle (Optional[str]): An optional subtitle to display below the title.
    """
    st.title(title)
    if subtitle:
        st.markdown(f"<h4 style='color:gray;'>{subtitle}</h4>", unsafe_allow_html=True)
