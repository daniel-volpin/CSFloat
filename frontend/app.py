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

# Top navigation links
nav_cols = st.columns([1, 1, 1])
with nav_cols[0]:
    st.page_link("app.py", label="Home")
with nav_cols[1]:
    st.page_link("pages/1_Analysis.py", label="Analysis")
with nav_cols[2]:
    st.page_link("pages/2_Settings.py", label="Settings")
st.markdown("---")

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
    st.caption("Use the filters above to refine your search. Navigate using the links at the top.")


# Main layout container - Home page content
with st.container():
    st.markdown("## Home")
    st.markdown("---")

    left, right = st.columns([2, 1])

    # Listings display (left)
    with left:
        items = []
        error_message = None
        # Only fetch listings if filters_applied is set
        if st.session_state.get("filters_applied", False):
            with st.spinner("Loading listings..."):
                try:
                    items = fetch_listings(params)
                except ApiClientError as e:
                    error_message = e.user_message
                except Exception:
                    error_message = "Unable to connect to backend service. Please ensure the backend server is running and reachable."
            # Debug output removed to keep UI clean
            # Store latest items for other pages (e.g., Analysis)
            st.session_state["last_items"] = items
            # Reset flag so next filter change triggers a new fetch
            st.session_state["filters_applied"] = False
        else:
            # Use last loaded items if present to avoid empty state on first render
            items = st.session_state.get("last_items", [])

        display_listings(items, error_message)

    st.markdown("")
    st.markdown("---")

    # Listing analysis section (right)
    with right:
        listing_analysis(items)
