import streamlit as st
from models.listing_models import ItemDTO

ITEM_FIELDS = {
    "price": "Price",
    "wear": "Wear",
    "rarity": "Rarity",
    "float_value": "Float Value",
    "name": "Name",
}


def render_item_card(item: ItemDTO) -> None:
    """
    Render a card UI for a single item listing.

    Args:
        item (ItemDTO): The item data transfer object to display.
    """
    st.markdown("---")
    if item.price is not None:
        st.write(f"**{ITEM_FIELDS['price']}:** ${item.price / 100:.2f}")
    else:
        st.write(f"**{ITEM_FIELDS['price']}:** N/A")
    st.write(f"**{ITEM_FIELDS['name']}:** {item.name if item.name else 'N/A'}")
    st.write(f"**{ITEM_FIELDS['wear']}:** {item.wear if item.wear else 'N/A'}")
    st.write(f"**{ITEM_FIELDS['rarity']}:** {item.rarity if item.rarity else 'N/A'}")
    st.write(
        f"**{ITEM_FIELDS['float_value']}:** "
        f"{item.float_value if item.float_value is not None else 'N/A'}"
    )
