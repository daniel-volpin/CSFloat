import os
import streamlit as st
from dotenv import load_dotenv

from api_client import fetch_listings
from components.item_display import display_item
from components.filters import filter_sidebar
from components.headers import custom_header
from config import APP_TITLE, APP_SUBTITLE


load_dotenv()

custom_header(APP_TITLE, subtitle=APP_SUBTITLE)


# Sidebar filters
params = filter_sidebar()
params = {k: v for k, v in params.items() if v is not None}

# Listings display

items = []
error_message = None
try:
    items = fetch_listings(params)
    if not items:
        with st.expander("Listings Results", expanded=True):
            st.warning("No listings found for the selected filters.")
except Exception:
    error_message = "Unable to connect to backend service. Please ensure the backend server is running and reachable."

if error_message:
    st.toast(error_message, icon="⚠️")
else:
    with st.expander("Listings Results", expanded=True):
        if items:
            for item in items:
                display_item(item)
