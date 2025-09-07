from __future__ import annotations

from typing import Dict, Tuple

import streamlit as st
from components.ui.basic_filters import render_basic_filters
from components.ui.float_and_rarity import render_float_and_rarity
from components.ui.item_details import render_item_details
from components.ui.misc_fields import render_misc_fields
from components.ui.price_filters import render_price_filters
from config.settings import CATEGORY_MAP, RARITY_MAP
from models.filter_models import FilterState


def filter_sidebar() -> Tuple[Dict[str, object], bool]:
    """Render the filter sidebar as a single form.

    Returns:
        params: Dict of API params derived from UI state
        submitted: True when the Apply button was pressed
    """
    with st.sidebar:
        with st.form("filters_form"):
            with st.expander("Basic Filters", expanded=True):
                cursor, limit, sort_by, category, def_index = render_basic_filters()

            with st.expander("Float & Rarity", expanded=False):
                min_float, max_float, rarity = render_float_and_rarity()

            with st.expander("Item Details", expanded=False):
                paint_seeds, paint_index, user_id, collection = render_item_details()

            market_hash_name, type_val, stickers = render_misc_fields()

            with st.expander("Price Filter", expanded=True):
                min_price, max_price = render_price_filters()

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
