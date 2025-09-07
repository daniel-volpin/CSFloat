from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import streamlit as st
from config.settings import (
    CATEGORY_MAP,
    CATEGORY_OPTIONS,
    DEFAULT_FLOAT_RANGE,
    DEFAULT_LIMIT,
    DEFAULT_SORT_INDEX,
    RARITY_MAP,
    RARITY_OPTIONS,
    SORT_OPTIONS,
)
from models.filter_models import FilterState

WIDGET_KEY_PREFIX = "filters_"


def _parse_csv_ints(raw: str | None) -> Optional[List[int]]:
    if not raw:
        return None
    values = [x.strip() for x in str(raw).split(",")]
    ints = [int(x) for x in values if x.isdigit()]
    return ints or None


def _render_basic_filters() -> Tuple[str, int, str, str, Optional[List[int]]]:
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
    def_index = _parse_csv_ints(def_index_raw)
    return cursor, limit, sort_by, category, def_index


def _render_float_and_rarity() -> Tuple[float, float, List[str]]:
    min_float, max_float = st.slider(
        "Float Range", 0.0, 1.0, DEFAULT_FLOAT_RANGE, step=0.01, key=f"{WIDGET_KEY_PREFIX}float"
    )
    rarity: List[str] = st.multiselect("Rarity", RARITY_OPTIONS, key=f"{WIDGET_KEY_PREFIX}rarity")
    return min_float, max_float, rarity


def _render_item_details() -> (
    Tuple[Optional[List[int]], Optional[int], Optional[str], Optional[str]]
):
    paint_seed_input = st.text_input(
        "Paint Seed (comma separated)", "", key=f"{WIDGET_KEY_PREFIX}paint_seed"
    )
    paint_seeds = _parse_csv_ints(paint_seed_input)

    paint_index_raw = st.text_input("Paint Index", "", key=f"{WIDGET_KEY_PREFIX}paint_index")
    paint_index = int(paint_index_raw) if paint_index_raw.strip().isdigit() else None

    user_id = st.text_input("User ID", "", key=f"{WIDGET_KEY_PREFIX}user_id") or None
    collection = st.text_input("Collection", "", key=f"{WIDGET_KEY_PREFIX}collection") or None
    return paint_seeds, paint_index, user_id, collection


def _render_misc_fields() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    market_hash_name = (
        st.text_input("Market Hash Name (manual search)", "", key=f"{WIDGET_KEY_PREFIX}mhn") or None
    )
    type_ = st.selectbox(
        "Type", ["", "buy_now", "auction"], index=0, key=f"{WIDGET_KEY_PREFIX}type"
    )
    type_val = type_ or None
    stickers = st.text_input("Stickers", "", key=f"{WIDGET_KEY_PREFIX}stickers") or None
    return market_hash_name, type_val, stickers


def _render_price_filters() -> Tuple[Optional[float], Optional[float]]:
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


def filter_sidebar() -> Tuple[Dict[str, object], bool]:
    """Render the filter sidebar as a single form.

    Returns:
        params: Dict of API params derived from UI state
        submitted: True when the Apply button was pressed
    """
    with st.sidebar:
        with st.form("filters_form"):
            with st.expander("Basic Filters", expanded=True):
                cursor, limit, sort_by, category, def_index = _render_basic_filters()

            with st.expander("Float & Rarity", expanded=False):
                min_float, max_float, rarity = _render_float_and_rarity()

            with st.expander("Item Details", expanded=False):
                paint_seeds, paint_index, user_id, collection = _render_item_details()

            market_hash_name, type_val, stickers = _render_misc_fields()

            with st.expander("Price Filter", expanded=True):
                min_price, max_price = _render_price_filters()

            state = FilterState(
                cursor=cursor or None,
                limit=limit,
                sort_by=sort_by,
                category=category,
                def_index=def_index,
                min_float=min_float,
                max_float=max_float,
                rarity_selections=rarity,
                paint_seed=paint_seeds,
                paint_index=paint_index,
                user_id=user_id,
                collection=collection,
                market_hash_name=market_hash_name,
                type=type_val,
                stickers=stickers,
                min_price=min_price,
                max_price=max_price,
            )

            params = state.to_params(category_map=CATEGORY_MAP, rarity_map=RARITY_MAP)
            submitted = st.form_submit_button("Apply Filters")
    return params, submitted
