import streamlit as st


def set_error_message(msg):
    st.session_state["last_error_message"] = msg


def get_error_message():
    return st.session_state.get("last_error_message", None)


def get_last_items():
    return st.session_state.get("last_items", [])


def set_last_items(items):
    st.session_state["last_items"] = items


def set_filters_applied(val: bool):
    st.session_state["filters_applied"] = val


def get_filters_applied():
    return st.session_state.get("filters_applied", False)


def set_analysis_fallback(open: bool, pos: str = "top"):
    st.session_state["analysis_fallback_open"] = open
    st.session_state["analysis_fallback_pos"] = pos


def get_analysis_fallback():
    return st.session_state.get("analysis_fallback_open"), st.session_state.get(
        "analysis_fallback_pos"
    )
