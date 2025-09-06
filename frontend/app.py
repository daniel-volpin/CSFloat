
import streamlit as st
import requests

# Centralized field names for maintainability
ITEM_FIELDS = {
    "price": "Price",
    "paint_seed": "Paint Seed",
    "float_value": "Float Value",
    "market_hash_name": "Market Hash Name",
    "item_name": "Item Name",
    "wear_name": "Wear Name",
    "inspect_link": "Inspect Link",
}

def display_item(item):
    st.markdown("---")
    # Price is always present
    st.write(f"**{ITEM_FIELDS['price']}:** ${item.get('price', 0) / 100:.2f}")
    # Nested item fields
    item_data = item.get('item', {})
    for key in ["paint_seed", "float_value", "market_hash_name", "item_name", "wear_name"]:
        if key in item_data and item_data[key] is not None:
            st.write(f"**{ITEM_FIELDS[key]}:** {item_data[key]}")
    # Inspect link
    if "inspect_link" in item_data and item_data["inspect_link"]:
        st.markdown(f"[{ITEM_FIELDS['inspect_link']}]({item_data['inspect_link']})")

st.title("CSFloat Listings")

# Sidebar for query parameters
st.sidebar.header("Filter Listings")
cursor = st.sidebar.text_input("Cursor", "")
limit = st.sidebar.slider("Limit", 1, 50, 10)
sort_by = st.sidebar.selectbox("Sort By", [
    "lowest_price", "highest_price", "most_recent", "expires_soon", "lowest_float", "highest_float", "best_deal", "highest_discount", "float_rank", "num_bids"
], index=6)
category = st.sidebar.selectbox("Category", ["Any", "Normal", "StatTrak", "Souvenir"], index=0)
category_map = {"Any": 0, "Normal": 1, "StatTrak": 2, "Souvenir": 3}
def_index = st.sidebar.text_input("Def Index (comma separated)", "")
min_float = st.sidebar.text_input("Min Float", "")
max_float = st.sidebar.text_input("Max Float", "")
rarity = st.sidebar.text_input("Rarity", "")
paint_seed = st.sidebar.text_input("Paint Seed", "")
paint_index = st.sidebar.text_input("Paint Index", "")
user_id = st.sidebar.text_input("User ID", "")
collection = st.sidebar.text_input("Collection", "")
min_price = st.sidebar.text_input("Min Price (cents)", "")
max_price = st.sidebar.text_input("Max Price (cents)", "")
market_hash_name = st.sidebar.text_input("Market Hash Name", "")
type_ = st.sidebar.selectbox("Type", ["", "buy_now", "auction"], index=0)
stickers = st.sidebar.text_input("Stickers", "")

params = {
    "cursor": cursor or None,
    "limit": limit,
    "sort_by": sort_by,
    "category": category_map[category],
    "def_index": [int(x) for x in def_index.split(",") if x.strip().isdigit()] if def_index else None,
    "min_float": float(min_float) if min_float else None,
    "max_float": float(max_float) if max_float else None,
    "rarity": rarity or None,
    "paint_seed": int(paint_seed) if paint_seed else None,
    "paint_index": int(paint_index) if paint_index else None,
    "user_id": user_id or None,
    "collection": collection or None,
    "min_price": int(min_price) if min_price else None,
    "max_price": int(max_price) if max_price else None,
    "market_hash_name": market_hash_name or None,
    "type": type_ or None,
    "stickers": stickers or None,
}

# Remove None values
params = {k: v for k, v in params.items() if v is not None}

try:
    response = requests.get("http://localhost:8000/api/listings", params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        st.info("No listings found for the selected filters.")
    for item in data:
        display_item(item)
except requests.RequestException as e:
    st.error(f"Failed to fetch listings: {e}")
