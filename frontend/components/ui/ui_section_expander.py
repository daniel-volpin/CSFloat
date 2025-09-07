from typing import Any

import streamlit as st


def render_expander(label: str, expanded: bool = False) -> Any:
    """
    Render a Streamlit expander section with the given label.

    Args:
        label (str): The label for the expander section.
        expanded (bool): Whether the expander is open by default.

    Returns:
        Any: The expander object for use as a context manager.
    """
    return st.expander(label, expanded=expanded)
