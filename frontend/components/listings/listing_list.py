import streamlit as st
from typing import List, Optional
from components.ui.item_card import display_item


def display_listings(items: Optional[List], error_message: Optional[str] = None):
    """
    Display listings and handle error/success feedback.
    Args:
        items: List of items to display.
        error_message: Optional error message to show.
    """
    st.markdown("### Listings")
    st.caption("Browse the latest items based on your selected filters.")
    st.write("")
    if error_message:
        st.error(error_message, icon="⚠️")
    else:
        st.markdown("#### Listings Results")
        if items:
            for item in items:
                display_item(item)
        else:
            st.warning("No listings found for the selected filters.")
