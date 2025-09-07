from typing import Any, List, Optional

import streamlit as st


def get_dialog() -> Optional[Any]:
    """
    Return the Streamlit dialog function if available, else None.

    Returns:
        Dialog function or None.
    """
    return getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)


def show_analysis_modal(items: List[Any]) -> bool:
    """
    Show analysis in a modal dialog if supported, else return False.

    Args:
        items: List of items to analyze.

    Returns:
        True if modal shown, else False.
    """
    Dialog = get_dialog()
    if Dialog is None:
        return False

    @Dialog("Analyze Listings")
    def _analysis_dialog():
        from components.listings.render_listings_analysis import render_listing_analysis

        render_listing_analysis(items)

    _analysis_dialog()
    return True


def show_analysis_fallback(items: List[Any], error_message: Optional[str]) -> None:
    """
    Show analysis in an expander as a fallback.

    Args:
        items: List of items to analyze.
        error_message: Optional error message to display.
    """
    with st.expander("💬 Quick Analysis", expanded=True):
        if error_message:
            st.error(error_message)
        from components.listings.render_listings_analysis import render_listing_analysis

        render_listing_analysis(items)
        if st.button("Close", key="analysis_fallback_close_top"):
            st.session_state["analysis_fallback_open"] = False
