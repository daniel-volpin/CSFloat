from typing import List, Optional

import streamlit as st
from client.backend_service import BackendApiError, BackendClient


def listing_analysis(items: Optional[List], default_model: Optional[str] = None):
    """
    Display AI-powered analysis interface for listings.
    Args:
        items: List of items to analyze.
        default_model: Default model name for AI analysis.
    """
    st.markdown("### Analyze Listings with AI")
    st.caption("Get insights or recommendations powered by AI.")
    st.write("")
    q = st.text_area(
        "Your question",
        placeholder="e.g., Best low-float AKs under $200? Which items look undervalued?",
        help="Type your question for the AI to analyze the current listings.",
    )
    max_items = st.slider(
        "Max items to analyze",
        10,
        200,
        50,
        step=10,
        help="Set the maximum number of listings the AI will consider in its analysis.",
    )
    custom_model = st.text_input(
        "Model (optional)",
        value=default_model or "gpt-4o-mini",
        help="Specify a custom model for AI analysis, or leave as default.",
    )
    if st.button(
        "Analyze Listings with AI",
        help="Click to get AI-powered insights based on your question and current listings.",
    ):
        if not items:
            st.warning("No listings loaded yet. Adjust filters and load listings first.")
        elif not q.strip():
            st.info("Enter a question to analyze the current listings.")
        else:
            with st.spinner("Thinking with AI..."):
                backend = BackendClient()
                try:
                    answer = backend.analyze_listings(
                        q.strip(), items, model=custom_model, max_items=max_items
                    )
                    st.success("AI analysis complete!")
                    st.markdown(answer)
                except BackendApiError as e:
                    st.error(e.args[0])
                except Exception:
                    st.error("Failed to get AI analysis. Please try again.")
