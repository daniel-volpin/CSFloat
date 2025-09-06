import streamlit as st
from client.csfloat_api import ApiClientError, fetch_listings
from components.listings.listing_filters import filter_sidebar
from components.listings.listing_insights import listing_analysis
from components.listings.listing_list import display_listings
from components.ui.main_header import custom_header
from config.settings import APP_SUBTITLE, APP_TITLE
from dotenv import load_dotenv

load_dotenv()


custom_header(APP_TITLE, subtitle=APP_SUBTITLE)


# Sidebar navigation and filters
with st.sidebar:
    st.title("CSFloat Navigation")
    nav_option = st.radio("Go to:", ["Home", "Analysis", "Settings"])
    st.markdown("---")
    st.markdown("#### Filters")
    params = filter_sidebar()
    params = {k: v for k, v in params.items() if v is not None}

    st.markdown("---")
    st.caption(
        "Use the filters above to refine your search. Navigate between sections using the radio buttons."
    )


# Main layout container
with st.container():
    st.markdown(f"## {nav_option} Section")
    st.markdown("---")

    if nav_option == "Home":
        left, right = st.columns([2, 1])

        # Listings display (left)
        with left:
            items = []
            error_message = None
            with st.spinner("Loading listings..."):
                try:
                    items = fetch_listings(params)
                except ApiClientError as e:
                    error_message = e.user_message
                except Exception:
                    error_message = "Unable to connect to backend service. Please ensure the backend server is running and reachable."
            display_listings(items, error_message)

        st.markdown("")
        st.markdown("---")

        # Listing analysis section (right)
        with right:
            listing_analysis(items)

    elif nav_option == "Analysis":
        st.markdown("### Analysis")
        st.info("Analysis tools and visualizations will appear here.")

    elif nav_option == "Settings":
        st.markdown("### Settings")
        st.info("Settings and configuration options will appear here.")
