from typing import Optional

import streamlit as st
from client.backend_client import ApiClientError, fetch_listings
from components.ui.item_card_display_ui import render_item_card


@st.cache_data
def get_cached_listings(params):
    try:
        return fetch_listings(params)
    except ApiClientError as e:
        st.error(e.user_message)
        return []
    except Exception:
        st.error(
            "Unable to connect to backend service. Please ensure the backend server is running and reachable."
        )
        return []


def render_listings(params: Optional[dict] = None, error_message: Optional[str] = None):
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
