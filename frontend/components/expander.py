import streamlit as st

def custom_expander(label: str, expanded: bool = False):
    return st.expander(label, expanded=expanded)
