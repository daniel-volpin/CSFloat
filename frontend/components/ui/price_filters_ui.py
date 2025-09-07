from typing import Optional, Tuple

import streamlit as st
from components.ui.item_filter_utils import WIDGET_KEY_PREFIX


def render_price_filters() -> Tuple[Optional[float], Optional[float]]:
    st.caption("Enter price in US dollars (e.g., 100 for $100)")
    col1, col2 = st.columns(2)
    min_price_dollars = col1.number_input(
        "Min Price ($ USD)",
        min_value=0.0,
        value=0.0,
        step=0.01,
        key=f"{WIDGET_KEY_PREFIX}min_price",
    )
    max_price_dollars = col2.number_input(
        "Max Price ($ USD)",
        min_value=0.0,
        value=0.0,
        step=0.01,
        key=f"{WIDGET_KEY_PREFIX}max_price",
    )
    min_price = float(min_price_dollars) if min_price_dollars > 0 else None
    max_price = float(max_price_dollars) if max_price_dollars > 0 else None
    return min_price, max_price
