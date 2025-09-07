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
    if filters_submitted:
        st.session_state["filters"] = params
        st.session_state["filters_applied"] = True

    active_params = st.session_state["filters"] if st.session_state["filters_applied"] else {}
    st.markdown("")
    items = None
    error_message = None

    col1, col2 = st.columns([1.2, 1.8], gap="large")
    with col1:
        st.markdown("<h2 style='margin-bottom:0.5em;'>Listings</h2>", unsafe_allow_html=True)
        if st.session_state["filters_applied"]:
            with st.spinner("Loading listings..."):
                items, error_message = fetch_and_store_listings(active_params)
            render_listings(items, error_message)
        else:
            st.info("Apply filters to see listings.")
    with col2:
        st.markdown(
            "<h2 style='margin-bottom:0.5em;'>Analyze Listings with AI</h2>", unsafe_allow_html=True
        )
        render_listing_analysis(items if items else [])


if __name__ == "__main__":
    main()
