import streamlit as st

from typing import Optional


def custom_header(title: str, subtitle: Optional[str] = None):
    st.title(title)
    if subtitle:
        st.markdown(f"<h4 style='color:gray;'>{subtitle}</h4>", unsafe_allow_html=True)
