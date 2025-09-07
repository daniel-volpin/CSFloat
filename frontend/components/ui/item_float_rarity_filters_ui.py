from typing import List, Tuple

import streamlit as st
from components.ui.item_filter_utils import WIDGET_KEY_PREFIX
from config.settings import DEFAULT_FLOAT_RANGE, RARITY_OPTIONS


def render_float_and_rarity() -> Tuple[float, float, List[str]]:
    """
    Render UI for float range and rarity selection.

    Returns:
        Tuple[float, float, List[str]]: Selected min float, max float, and list of selected rarities.
    """
    min_float, max_float = st.slider(
        "Float Range", 0.0, 1.0, DEFAULT_FLOAT_RANGE, step=0.01, key=f"{WIDGET_KEY_PREFIX}float"
    )
    rarity: List[str] = st.multiselect("Rarity", RARITY_OPTIONS, key=f"{WIDGET_KEY_PREFIX}rarity")
    return min_float, max_float, rarity
