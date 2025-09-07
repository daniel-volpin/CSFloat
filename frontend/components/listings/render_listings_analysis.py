from typing import Any, List, Optional

import streamlit as st
from client.backend_client import BackendApiError, BackendClient


def render_listing_analysis(
    items: Optional[List[Any]], default_model: Optional[str] = None
) -> None:
    """
    Display AI-powered analysis interface for listings.
    Args:
        items: List of items to analyze.
        default_model: Default model name for AI analysis.
    """
    # --- UI Inputs ---
    q = st.text_area(
        "Your question",
        placeholder="e.g., Best low-float AKs under $200? Which items look undervalued?",
        help="Type your question for the AI to analyze the current listings.",
    )
    st.write("")
    max_items = st.slider(
        "Max items to analyze",
        10,
        200,
        50,
        step=10,
        help="Set the maximum number of listings the AI will consider in its analysis.",
    )
    st.write("")

    # --- Model Selection ---
    backend = BackendClient()
    try:
        model_options = backend.list_llm_models()
    except BackendApiError:
        model_options = []
    options_labels = [m.get("label", m.get("value", "")) for m in model_options]
    options_values = [m.get("value") for m in model_options]
    options_labels.append("Custom…")
    options_values.append(None)
    selected_label = st.selectbox(
        "Model",
        options_labels,
        index=0,
        help="Choose an AI model for analysis or enter a custom model below.",
    )
    selected_value = (
        options_values[options_labels.index(selected_label)]
        if selected_label in options_labels
        else None
    )
    if selected_value is None:
        custom_model = st.text_input(
            "Custom model",
            value=default_model or "gpt-4o-mini",
            help=(
                "Specify a model (e.g., gpt-4o-mini). "
                "Use prefixes to force provider: openai:<model> or lmstudio:<model_key>."
            ),
        )
    else:
        custom_model = selected_value
    st.write("")

    # --- Analysis Trigger ---
    if st.button(
        "🔍 Analyze Listings with AI",
        help="Click to get AI-powered insights based on your question and current listings.",
        use_container_width=True,
    ):
        st.write("")
        if not items:
            st.warning("No listings loaded yet. Adjust filters and load listings first.")
        elif not q.strip():
            st.info("Enter a question to analyze the current listings.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = backend.analyze_listings(
                        q.strip(), items, model=custom_model, max_items=max_items
                    )
                    st.success("AI analysis complete!")
                    st.markdown(
                        f"<div style='background:#23272f;padding:18px 20px;border-radius:10px;margin-top:10px;box-shadow:0 2px 12px rgba(0,0,0,0.18);'>"
                        f"<span style='font-size:1.1em;'>{answer}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                except BackendApiError as e:
                    st.error(e.args[0])
                except Exception:
                    st.error("Failed to get AI analysis. Please try again.")
