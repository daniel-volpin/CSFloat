from typing import Any

import streamlit as st
from components.listings.render_listings import render_listings
from utils.dialogs import show_analysis_fallback, show_analysis_modal
from utils.listings import fetch_and_store_listings
from utils.session import get_analysis_fallback, get_error_message, get_last_items


def render_home_tab(params: Any) -> None:
    """
    Render the home tab UI, including listings and analysis.

    Args:
        params: Query/filter parameters for listings.
    """
    st.markdown("---")
    items = get_last_items()
    error_message = get_error_message()
    from utils.session import get_filters_applied

    if get_filters_applied():
        with st.spinner("Loading listings..."):
            items, error_message = fetch_and_store_listings(params)
    top_spacer, top_action_col = st.columns([6, 1])
    with top_action_col:
        if st.button("💬 Analyze", key="analysis_quick_top"):
            opened = show_analysis_modal(items)
            if not opened:
                from utils.session import set_analysis_fallback

                set_analysis_fallback(True, "top")
            items = get_last_items()
    fallback_open, fallback_pos = get_analysis_fallback()
    if fallback_open and fallback_pos == "top":
        show_analysis_fallback(items, error_message)
    if items:
        render_listings(params, error_message)
    elif error_message:
        st.error(error_message)
    else:
        st.info("No listings to display. Please apply filters to fetch items.")
