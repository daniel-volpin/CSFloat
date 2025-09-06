

import streamlit as st
from api_client import fetch_listings
from components import display_item

st.title("CSFloat Listings")

# Sidebar for query parameters
st.sidebar.header("Filter Listings")

with st.sidebar.expander("Basic Filters", expanded=True):
    cursor = st.text_input("Cursor", "")
    limit = st.slider("Limit", 1, 50, 10)
    sort_by = st.selectbox("Sort By", [
        "lowest_price", "highest_price", "most_recent", "expires_soon", "lowest_float", "highest_float", "best_deal", "highest_discount", "float_rank", "num_bids"
    ], index=6)
    category = st.selectbox("Category", ["Any", "Normal", "StatTrak", "Souvenir"], index=0)
    category_map = {"Any": 0, "Normal": 1, "StatTrak": 2, "Souvenir": 3}
    def_index = st.text_input("Def Index (comma separated)", "")

with st.sidebar.expander("Float & Rarity", expanded=False):
    min_float, max_float = st.slider("Float Range", 0.0, 1.0, (0.0, 1.0), step=0.01)
    rarity_options = ["", "Common", "Uncommon", "Rare", "Mythical", "Legendary", "Ancient", "Immortal"]
    rarity = st.multiselect("Rarity", rarity_options)

with st.sidebar.expander("Item Details", expanded=False):
    paint_seed = st.text_input("Paint Seed", "")
    paint_index = st.text_input("Paint Index", "")
    user_id = st.text_input("User ID", "")
    collection = st.text_input("Collection", "")
    market_hash_name = st.text_input("Market Hash Name", "")
    type_ = st.selectbox("Type", ["", "buy_now", "auction"], index=0)
    stickers = st.text_input("Stickers", "")

with st.sidebar.expander("Price Filter", expanded=True):
    col1, col2 = st.columns(2)
    min_price_dollars = col1.number_input("Min Price ($)", min_value=0.0, value=0.0, step=0.01)
    max_price_dollars = col2.number_input("Max Price ($)", min_value=0.0, value=0.0, step=0.01)

params = {
    "cursor": cursor or None,
    "limit": limit,
    "sort_by": sort_by,
    "category": category_map[category],
    "def_index": [int(x) for x in def_index.split(",") if x.strip().isdigit()] if def_index else None,
    "min_float": min_float,
    "max_float": max_float,
    "rarity": ",".join(rarity) if rarity else None,
    "paint_seed": int(paint_seed) if paint_seed else None,
    "paint_index": int(paint_index) if paint_index else None,
    "user_id": user_id or None,
    "collection": collection or None,
    "min_price": int(min_price_dollars * 100) if min_price_dollars else None,
    "max_price": int(max_price_dollars * 100) if max_price_dollars else None,
    "market_hash_name": market_hash_name or None,
    "type": type_ or None,
    "stickers": stickers or None,
}

# Remove None values
params = {k: v for k, v in params.items() if v is not None}


with st.expander("Listings Results", expanded=True):
    try:
        items = fetch_listings(params)
        if not items:
            st.info("No listings found for the selected filters.")
        for item in items:
            display_item(item)
    except Exception as e:
        st.error(f"Failed to fetch listings: {e}")
