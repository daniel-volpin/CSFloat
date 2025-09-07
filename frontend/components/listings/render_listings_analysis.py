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
    # Persist analysis panel state, but do NOT affect global state
    q = st.text_area(
        "Your question",
        value=st.session_state.get("analysis_question", ""),
        placeholder="e.g., Best low-float AKs under $200? Which items look undervalued?",
        help="Type your question for the AI to analyze the current listings.",
        key="analysis_question_input",
    )
    st.session_state["analysis_question"] = q
    st.write("")
    max_items = st.slider(
        "Max items to analyze",
        10,
        200,
        st.session_state.get("analysis_max_items", 50),
        step=10,
        help="Set the maximum number of listings the AI will consider in its analysis.",
        key="analysis_max_items_slider",
    )
    st.session_state["analysis_max_items"] = max_items
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
        index=(
            options_labels.index(st.session_state.get("analysis_selected_label", options_labels[0]))
            if st.session_state.get("analysis_selected_label", options_labels[0]) in options_labels
            else 0
        ),
        help="Choose an AI model for analysis or enter a custom model below.",
        key="analysis_model_select",
    )
    st.session_state["analysis_selected_label"] = selected_label
    selected_value = (
        options_values[options_labels.index(selected_label)]
        if selected_label in options_labels
        else None
    )
    if selected_value is None:
        custom_model = st.text_input(
            "Custom model",
            value=st.session_state.get("analysis_custom_model", default_model or "gpt-4o-mini"),
            help=(
                "Specify a model (e.g., gpt-4o-mini). "
                "Use prefixes to force provider: openai:<model> or lmstudio:<model_key>."
            ),
            key="analysis_custom_model_input",
        )
        st.session_state["analysis_custom_model"] = custom_model
    else:
        custom_model = selected_value
        st.session_state["analysis_custom_model"] = custom_model
    st.write("")

    # --- Analysis Trigger ---
    @st.cache_data(show_spinner=False)
    def cached_analyze_listings(q, items, model, max_items):
        return backend.analyze_listings(q, items, model=model, max_items=max_items)

    q_str = q if isinstance(q, str) else ""
    analyze_disabled = not items
    analyze_help = (
        "Listings must be loaded before analysis can run. Apply filters first."
        if analyze_disabled
        else "Click to get AI-powered insights based on your question and current listings."
    )
    analyze_btn = st.button(
        "🔍 Analyze Listings with AI",
        help=analyze_help,
        use_container_width=True,
        disabled=analyze_disabled,
    )
    if analyze_btn:
        st.write("")
        if not q_str.strip():
            st.info("Enter a question to analyze the current listings.")
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = cached_analyze_listings(q_str.strip(), items, custom_model, max_items)
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
