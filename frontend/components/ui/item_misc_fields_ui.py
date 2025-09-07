from typing import Optional, Tuple

import streamlit as st
from components.ui.item_filter_utils import WIDGET_KEY_PREFIX


def render_misc_fields() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Render UI for miscellaneous item fields (market hash name, type, stickers).

    Returns:
        Tuple[Optional[str], Optional[str], Optional[str]]: Market hash name, type, stickers.
    """
    market_hash_name = (
        st.text_input("Market Hash Name (manual search)", "", key=f"{WIDGET_KEY_PREFIX}mhn") or None
    )
    type_ = st.selectbox(
        "Type", ["", "buy_now", "auction"], index=0, key=f"{WIDGET_KEY_PREFIX}type"
    )
    type_val = type_ or None
    stickers = st.text_input("Stickers", "", key=f"{WIDGET_KEY_PREFIX}stickers") or None
    return market_hash_name, type_val, stickers
