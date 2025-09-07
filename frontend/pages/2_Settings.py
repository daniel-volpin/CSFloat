import streamlit as st
from components.ui.main_header import custom_header
from config.settings import APP_SUBTITLE, APP_TITLE

custom_header(APP_TITLE, subtitle=APP_SUBTITLE)

# Top navigation links
nav_cols = st.columns([1, 1, 1])
with nav_cols[0]:
    st.page_link("app.py", label="Home")
with nav_cols[1]:
    st.page_link("pages/1_Analysis.py", label="Analysis")
with nav_cols[2]:
    st.page_link("pages/2_Settings.py", label="Settings")
st.markdown("---")

st.markdown("## Settings")
st.markdown("---")
st.info("Settings and configuration options will appear here.")
