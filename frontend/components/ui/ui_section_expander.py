import streamlit as st


def render_expander(label: str, expanded: bool = False):
    return st.expander(label, expanded=expanded)
