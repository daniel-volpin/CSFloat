import streamlit as st
from client.backend_client import ApiClientError, fetch_listings
from components.listings.filter_sidebar import filter_sidebar
from components.listings.listing_insights import listing_analysis
from components.listings.listing_list import display_listings
from components.ui.main_header import custom_header
from config.settings import APP_SUBTITLE, APP_TITLE
from dotenv import load_dotenv

load_dotenv()


custom_header(APP_TITLE, subtitle=APP_SUBTITLE)

# Top navigation as tabs for clarity
tabs = st.tabs(["Home", "Analysis", "Settings"])

# Sidebar filters
with st.sidebar:
    st.markdown("#### Filters")

# Render filters form and collect submission outside to avoid double nesting
params, filters_submitted = filter_sidebar()
params = {k: v for k, v in params.items() if v is not None}
if filters_submitted:
    st.session_state["filters_applied"] = True

with st.sidebar:
    st.markdown("---")
    st.caption("Use the filters above to refine your search.")

with tabs[0]:
    st.markdown("---")
    items = []
    error_message = None
    # Fetch listings only when filters are applied
    if st.session_state.get("filters_applied", False):
        with st.spinner("Loading listings..."):
            try:
                items = fetch_listings(params)
            except ApiClientError as e:
                error_message = e.user_message
            except Exception:
                error_message = "Unable to connect to backend service. Please ensure the backend server is running and reachable."
        # Store latest items for other tabs
        st.session_state["last_items"] = items
        # Reset flag so next filter change triggers a new fetch
        st.session_state["filters_applied"] = False
    else:
        # Use last loaded items if present to avoid empty state on first render
        items = st.session_state.get("last_items", [])

    display_listings(items, error_message)

with tabs[1]:
    st.markdown("---")
    items_for_analysis = st.session_state.get("last_items", [])
    if not items_for_analysis:
        st.info("No listings loaded yet. Use Home filters and apply.")
    listing_analysis(items_for_analysis)

with tabs[2]:
    st.markdown("---")
    st.info("Settings and configuration options will appear here.")
