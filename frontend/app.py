import streamlit as st
from api_client import fetch_listings
from components.item_display import display_item
from components.filters import filter_sidebar
from components.headers import custom_header
from config import APP_TITLE, APP_SUBTITLE


custom_header(APP_TITLE, subtitle=APP_SUBTITLE)

# Get filter params from sidebar
params = filter_sidebar()

# Remove None values
params = {k: v for k, v in params.items() if v is not None}


with st.expander("Listings Results", expanded=True):
    try:
        items = fetch_listings(params)
        if not items:
            st.info("No listings found for the selected filters.")
        for item in items:
            display_item(item)
    except Exception as e:
        st.error(f"Failed to fetch listings: {e}")
