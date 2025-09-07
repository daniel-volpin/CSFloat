import streamlit as st
from client.backend_client import ApiClientError, fetch_listings
from components.listings.filter_sidebar import filter_sidebar
from components.listings.listing_insights import listing_analysis
from components.listings.listing_list import display_listings
from components.ui.main_header import render_header
from config.settings import APP_SUBTITLE, APP_TITLE
from dotenv import load_dotenv

load_dotenv()


render_header(APP_TITLE, subtitle=APP_SUBTITLE)

# Modal dialog compatibility (uses st.dialog if available, else experimental)
Dialog = getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)


def open_analysis_modal(items):
    """Open analysis UI in a modal if supported. Returns True if opened."""
    if Dialog is None:
        return False

    @Dialog("Analyze Listings")
    def _analysis_dialog():
        listing_analysis(items)

    _analysis_dialog()
    return True


# Top navigation as tabs for clarity (Analysis via modal only)
tabs = st.tabs(["Home", "Settings"])

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

    # Top Analyze action
    top_spacer, top_action_col = st.columns([6, 1])
    with top_action_col:
        if st.button("💬 Analyze", key="analysis_quick_top"):
            opened = open_analysis_modal(items)
            if not opened:
                st.session_state["analysis_fallback_open"] = True
                st.session_state["analysis_fallback_pos"] = "top"

    # Fallback inline expander at top if dialog is not available
    if (
        st.session_state.get("analysis_fallback_open")
        and st.session_state.get("analysis_fallback_pos") == "top"
    ):
        with st.expander("💬 Quick Analysis", expanded=True):
            listing_analysis(items)
            if st.button("Close", key="analysis_fallback_close_top"):
                st.session_state["analysis_fallback_open"] = False

    # Listings
    display_listings(items, error_message)

with tabs[1]:
    st.markdown("---")
    st.info("Settings and configuration options will appear here.")
