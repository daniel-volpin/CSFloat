from typing import List, Optional, Tuple

import streamlit as st
from components.ui.filter_utils import WIDGET_KEY_PREFIX, parse_csv_ints
from config.settings import CATEGORY_OPTIONS, DEFAULT_LIMIT, DEFAULT_SORT_INDEX, SORT_OPTIONS


def render_basic_filters() -> Tuple[str, int, str, str, Optional[List[int]]]:
    cursor = st.text_input("Cursor", "", key=f"{WIDGET_KEY_PREFIX}cursor")
    limit = st.slider("Limit", 1, 50, DEFAULT_LIMIT, key=f"{WIDGET_KEY_PREFIX}limit")
    sort_by = st.selectbox(
        "Sort By", SORT_OPTIONS, index=DEFAULT_SORT_INDEX, key=f"{WIDGET_KEY_PREFIX}sort_by"
    )
    category = st.selectbox(
        "Category", CATEGORY_OPTIONS, index=0, key=f"{WIDGET_KEY_PREFIX}category"
    )
    def_index_raw = st.text_input(
        "Def Index (comma separated)", "", key=f"{WIDGET_KEY_PREFIX}def_index"
    )
    def_index = parse_csv_ints(def_index_raw)
    return cursor, limit, sort_by, category, def_index
