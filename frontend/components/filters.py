import streamlit as st
from config import (
    DEFAULT_LIMIT,
    DEFAULT_FLOAT_RANGE,
    RARITY_OPTIONS,
    CATEGORY_OPTIONS,
    CATEGORY_MAP,
    SORT_OPTIONS,
)


def filter_sidebar():
    st.sidebar.header("Filter Listings")
    with st.sidebar.expander("Basic Filters", expanded=True):
        cursor = st.text_input("Cursor", "")
        limit = st.slider("Limit", 1, 50, DEFAULT_LIMIT)
        sort_by = st.selectbox("Sort By", SORT_OPTIONS, index=6)
        category = st.selectbox("Category", CATEGORY_OPTIONS, index=0)
        def_index = st.text_input("Def Index (comma separated)", "")
    with st.sidebar.expander("Float & Rarity", expanded=False):
        min_float, max_float = st.slider(
            "Float Range", 0.0, 1.0, DEFAULT_FLOAT_RANGE, step=0.01
        )
        rarity = st.multiselect("Rarity", RARITY_OPTIONS)
    with st.sidebar.expander("Item Details", expanded=False):
        paint_seed_input = st.text_input("Paint Seed (comma separated)", "")
        paint_seeds = (
            [int(x.strip()) for x in paint_seed_input.split(",") if x.strip().isdigit()]
            if paint_seed_input
            else None
        )
        paint_index = st.text_input("Paint Index", "")
        user_id = st.text_input("User ID", "")
        collection = st.text_input("Collection", "")
        # Fetch available item names from API
        from api_client import fetch_listings

        @st.cache_data(show_spinner=False)
        def get_item_names():
            params = {"limit": 50}
            # Only include params that are not None, not empty string, and not empty list
            clean_params = {}
            for k, v in params.items():
                if v is None:
                    continue
                if isinstance(v, str) and v.strip() == "":
                    continue
                if isinstance(v, list) and len(v) == 0:
                    continue
                clean_params[k] = v
            items = fetch_listings(clean_params)
            names = sorted(
                set(
                    [item.name for item in items if hasattr(item, "name") and item.name]
                )
            )
            return names

        item_names = get_item_names()
    item_name = st.selectbox("Item Name", ["Any"] + item_names, index=0)
    market_hash_name = st.text_input("Market Hash Name (manual search)", "")
    type_ = st.selectbox("Type", ["", "buy_now", "auction"], index=0)
    stickers = st.text_input("Stickers", "")
    with st.sidebar.expander("Price Filter", expanded=True):
        col1, col2 = st.columns(2)
        min_price_dollars = col1.number_input(
            "Min Price ($)", min_value=0.0, value=0.0, step=0.01
        )
        max_price_dollars = col2.number_input(
            "Max Price ($)", min_value=0.0, value=0.0, step=0.01
        )
    # ...existing code...
    # If you need ItemDTO or other models, use: from models import ItemDTO
    params = {
        "cursor": cursor or None,
        "limit": limit,
        "sort_by": sort_by,
        "category": CATEGORY_MAP[category],
        "def_index": (
            [int(x) for x in def_index.split(",") if x.strip().isdigit()]
            if def_index
            else None
        ),
        "min_float": min_float,
        "max_float": max_float,
        "rarity": ",".join(rarity) if rarity else None,
        "paint_seed": paint_seeds if paint_seeds else None,
        "paint_index": int(paint_index) if paint_index else None,
        "user_id": user_id or None,
        "collection": collection or None,
        "min_price": int(min_price_dollars * 100) if min_price_dollars else None,
        "max_price": int(max_price_dollars * 100) if max_price_dollars else None,
        "item_name": None if item_name == "Any" else item_name,
        "market_hash_name": market_hash_name or None,
        "type": type_ or None,
        "stickers": stickers or None,
    }
    params = {k: v for k, v in params.items() if v is not None}
    return params
