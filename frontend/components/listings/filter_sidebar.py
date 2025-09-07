import streamlit as st
from config.settings import (
    CATEGORY_MAP,
    CATEGORY_OPTIONS,
    DEFAULT_FLOAT_RANGE,
    DEFAULT_LIMIT,
    RARITY_OPTIONS,
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
    RARITY_MAP = {
        "": None,
        "Common": 1,
        "Uncommon": 2,
        "Rare": 3,
        "Mythical": 4,
        "Legendary": 5,
        "Ancient": 6,
        "Immortal": 7,
    }
    with st.sidebar.expander("Float & Rarity", expanded=False):
        min_float, max_float = st.slider("Float Range", 0.0, 1.0, DEFAULT_FLOAT_RANGE, step=0.01)
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
    market_hash_name = st.text_input("Market Hash Name (manual search)", "")
    type_ = st.selectbox("Type", ["", "buy_now", "auction"], index=0)
    stickers = st.text_input("Stickers", "")
    with st.sidebar.expander("Price Filter", expanded=True):
        st.caption("Enter price in US dollars (e.g., 100 for $100)")
        col1, col2 = st.columns(2)
        min_price_dollars = col1.number_input(
            "Min Price ($ USD)", min_value=0.0, value=0.0, step=0.01
        )
        max_price_dollars = col2.number_input(
            "Max Price ($ USD)", min_value=0.0, value=0.0, step=0.01
        )
    params = {
        "cursor": cursor or None,
        "limit": limit,
        "sort_by": sort_by,
        "category": CATEGORY_MAP[category],
        "def_index": (
            [int(x) for x in def_index.split(",") if x.strip().isdigit()] if def_index else None
        ),
        "min_float": min_float,
        "max_float": max_float,
        "rarity": (RARITY_MAP[rarity[0]] if rarity and len(rarity) == 1 else None),
        "paint_seed": paint_seeds if paint_seeds else None,
        "paint_index": int(paint_index) if paint_index else None,
        "user_id": user_id if user_id else None,
        "collection": collection if collection else None,
        "market_hash_name": market_hash_name if market_hash_name else None,
        "type": type_ if type_ else None,
        "stickers": stickers if stickers else None,
        # Send prices in dollars; backend converts to cents for upstream API
        "min_price": float(min_price_dollars) if min_price_dollars > 0 else None,
        "max_price": float(max_price_dollars) if max_price_dollars > 0 else None,
    }
    st.sidebar.write("Filter params:", params)
    return params
