import streamlit as st
from components.listings.render_filter_sidebar import filter_sidebar
from components.ui.app_main_header_ui import render_header
from config.settings import APP_SUBTITLE, APP_TITLE
from dotenv import load_dotenv
from pages.home import render_home_tab
from pages.settings import render_settings_tab


def main() -> None:
    """
    Main entry point for the Streamlit app.
    """
    load_dotenv()
    render_header(APP_TITLE, subtitle=APP_SUBTITLE)
    tabs = st.tabs(["Home", "Settings"])
    with st.sidebar:
        st.markdown("#### Filters")
    params, filters_submitted = filter_sidebar()
    params = {k: v for k, v in params.items() if v is not None}
    if filters_submitted:
        from utils.session import set_filters_applied

        set_filters_applied(True)
    with st.sidebar:
        st.markdown("---")
        st.caption("Use the filters above to refine your search.")
    with tabs[0]:
        render_home_tab(params)
    with tabs[1]:
        render_settings_tab()


if __name__ == "__main__":
    main()
