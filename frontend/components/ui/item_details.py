from typing import List, Optional, Tuple

import streamlit as st
from components.ui.filter_utils import WIDGET_KEY_PREFIX, parse_csv_ints


def render_item_details() -> (
    Tuple[Optional[List[int]], Optional[int], Optional[str], Optional[str]]
):
    paint_seed_input = st.text_input(
        "Paint Seed (comma separated)", "", key=f"{WIDGET_KEY_PREFIX}paint_seed"
    )
    paint_seeds = parse_csv_ints(paint_seed_input)
    paint_index_raw = st.text_input("Paint Index", "", key=f"{WIDGET_KEY_PREFIX}paint_index")
    paint_index = int(paint_index_raw) if paint_index_raw.strip().isdigit() else None
    user_id = st.text_input("User ID", "", key=f"{WIDGET_KEY_PREFIX}user_id") or None
    collection = st.text_input("Collection", "", key=f"{WIDGET_KEY_PREFIX}collection") or None
    return paint_seeds, paint_index, user_id, collection
