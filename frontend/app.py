import streamlit as st
import os
from dotenv import load_dotenv

from api_client import fetch_listings
from components.item_display import display_item
from components.filters import filter_sidebar
from components.headers import custom_header
from config import APP_TITLE, APP_SUBTITLE
from llm_client import ask_about_listings


load_dotenv()

custom_header(APP_TITLE, subtitle=APP_SUBTITLE)


# Sidebar filters
params = filter_sidebar()
params = {k: v for k, v in params.items() if v is not None}

# Listings display

items = []
error_message = None
try:
    items = fetch_listings(params)
    if not items:
        with st.expander("Listings Results", expanded=True):
            st.warning("No listings found for the selected filters.")
except Exception:
    error_message = "Unable to connect to backend service. Please ensure the backend server is running and reachable."

if error_message:
    st.toast(error_message, icon="⚠️")
else:
    with st.expander("Listings Results", expanded=True):
        if items:
            for item in items:
                display_item(item)

# LLM analysis section (independent of fetching/search)
with st.expander("Ask AI about current listings", expanded=False):
    q = st.text_area(
        "Your question",
        placeholder="e.g., Best low-float AKs under $200? Which items look undervalued?",
    )
    col_a, col_b = st.columns(2)
    max_items = col_a.slider("Max items to analyze", 10, 200, 50, step=10)
    custom_model = col_b.text_input(
        "Model (optional)",
        value=os.getenv("OPENAI_MODEL") or "gpt-4o",
    )
    if st.button("Analyze Listings with AI"):
        if not items:
            st.warning("No listings loaded yet. Adjust filters and load listings first.")
        elif not q.strip():
            st.info("Enter a question to analyze the current listings.")
        else:
            with st.spinner("Thinking with AI..."):
                answer = ask_about_listings(q.strip(), items, model=custom_model, max_items=max_items)
            st.markdown(answer)
