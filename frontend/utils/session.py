from typing import Any, List, Optional, Tuple

import streamlit as st


def set_error_message(msg: Optional[str]) -> None:
    """
    Set the last error message in session state.

    Args:
        msg: Error message string or None.
    """
    st.session_state["last_error_message"] = msg


def get_error_message() -> Optional[str]:
    """
    Get the last error message from session state.

    Returns:
        Error message string or None.
    """
    return st.session_state.get("last_error_message", None)


def get_last_items() -> List[Any]:
    """
    Get the last items from session state.

    Returns:
        List of items.
    """
    return st.session_state.get("last_items", [])


def set_last_items(items: List[Any]) -> None:
    """
    Set the last items in session state.

    Args:
        items: List of items.
    """
    st.session_state["last_items"] = items


def set_filters_applied(val: bool) -> None:
    """
    Set whether filters have been applied in session state.

    Args:
        val: True if filters applied, else False.
    """
    st.session_state["filters_applied"] = val


def get_filters_applied() -> bool:
    """
    Get whether filters have been applied from session state.

    Returns:
        True if filters applied, else False.
    """
    return st.session_state.get("filters_applied", False)


def set_analysis_fallback(open: bool, pos: str = "top") -> None:
    """
    Set analysis fallback state in session.

    Args:
        open: Whether fallback is open.
        pos: Position of fallback (default "top").
    """
    st.session_state["analysis_fallback_open"] = open
    st.session_state["analysis_fallback_pos"] = pos


def get_analysis_fallback() -> Tuple[Optional[bool], Optional[str]]:
    """
    Get analysis fallback state from session.

    Returns:
        Tuple of (open, pos).
    """
    return st.session_state.get("analysis_fallback_open"), st.session_state.get(
        "analysis_fallback_pos"
    )
