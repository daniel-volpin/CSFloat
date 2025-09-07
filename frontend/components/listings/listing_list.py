from typing import Optional

import streamlit as st
from client.backend_client import fetch_listings
from components.ui.item_card import render_item_card


@st.cache_data
def get_cached_listings(params):
    return fetch_listings(params)


def display_listings(params: Optional[dict] = None, error_message: Optional[str] = None):
    """
    Display listings and handle error/success feedback.
    Args:
        params: Query parameters for fetching listings.
        error_message: Optional error message to show.
    """
    st.markdown("### Listings")
    st.caption("Browse the latest items based on your selected filters.")
    st.write("")
    if error_message:
        st.error(error_message, icon="⚠️")
    else:
        st.markdown("#### Listings Results")
        items = get_cached_listings(params) if params else []
        if items:
            for item in items:
                render_item_card(item)
        else:
            st.warning("No listings found for the selected filters.")
