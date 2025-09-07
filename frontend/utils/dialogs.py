import streamlit as st


def get_dialog():
    """Return the Streamlit dialog function if available, else None."""
    return getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)


def show_analysis_modal(items):
    """Show analysis in a modal dialog if supported, else return False."""
    Dialog = get_dialog()
    if Dialog is None:
        return False

    @Dialog("Analyze Listings")
    def _analysis_dialog():
        from components.listings.render_listings_analysis import render_listing_analysis

        render_listing_analysis(items)

    _analysis_dialog()
    return True


def show_analysis_fallback(items, error_message):
    """Show analysis in an expander as a fallback."""
    with st.expander("💬 Quick Analysis", expanded=True):
        if error_message:
            st.error(error_message)
        from components.listings.render_listings_analysis import render_listing_analysis

        render_listing_analysis(items)
        if st.button("Close", key="analysis_fallback_close_top"):
            st.session_state["analysis_fallback_open"] = False
