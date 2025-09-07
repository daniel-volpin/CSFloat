import streamlit as st
from components.listings.render_filter_sidebar import filter_sidebar
from components.listings.render_listings import render_listings
from components.listings.render_listings_analysis import render_listing_analysis
from components.ui.app_main_header_ui import render_header
from config.settings import APP_SUBTITLE, APP_TITLE
from dotenv import load_dotenv
from utils.listings import fetch_and_store_listings


def main() -> None:
    """
    Main entry point for the Streamlit app.
    """
    load_dotenv()
    render_header(APP_TITLE, subtitle=APP_SUBTITLE)
    params, filters_submitted = filter_sidebar()
    params = {k: v for k, v in params.items() if v is not None}

    # Persist filter values in session_state
    if "filters" not in st.session_state:
        st.session_state["filters"] = {}
    if "filters_applied" not in st.session_state:
        st.session_state["filters_applied"] = False

    # Only update filters if user submits the form
    if filters_submitted:
        st.session_state["filters"] = params
        st.session_state["filters_applied"] = True
        st.rerun()

    # Reset Filters button
    if st.button("Reset Filters", key="reset_filters"):
        st.session_state["filters"] = {}
        st.session_state["filters_applied"] = False
        st.rerun()

    active_params = st.session_state["filters"] if st.session_state["filters_applied"] else {}
    st.markdown("")

    @st.cache_data(show_spinner=False)
    def cached_fetch_and_store_listings(params):
        return fetch_and_store_listings(params)

    items = None
    error_message = None
    if st.session_state["filters_applied"]:
        with st.spinner("Loading listings..."):
            items, error_message = cached_fetch_and_store_listings(active_params)

    col1, col2 = st.columns([1.2, 1.8], gap="large")
    with col1:
        st.markdown("<h2 style='margin-bottom:0.5em;'>Listings</h2>", unsafe_allow_html=True)
        if items:
            render_listings(items, error_message)
        else:
            st.info("Apply filters to see listings.")
    with col2:
        st.markdown(
            "<h2 style='margin-bottom:0.5em;'>Analyze Listings with AI</h2>", unsafe_allow_html=True
        )
        # Only show analysis if listings are loaded
        if items:
            st.markdown("Analyze the currently loaded listings using AI.")
            render_listing_analysis(items)
        else:
            st.info("Apply filters and load listings to enable analysis.")


if __name__ == "__main__":
    main()
