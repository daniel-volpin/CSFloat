from typing import Any, Dict, List, Optional

import streamlit as st
from client.backend_client import ApiClientError, fetch_listings
from models.listing_models import ItemDTO


@st.cache_data
def get_cached_listings(params: Optional[Dict[str, Any]]) -> List[dict]:
    """
    Fetch and cache listings from backend, handling errors centrally.
    Args:
        params: Query parameters for listings API.
    Returns:
        List of items.
    """
    try:
        safe_params = params if params is not None else {}
        items = fetch_listings(safe_params)
        if isinstance(items, tuple):
            items = items[0]
        if isinstance(items, ItemDTO):
            items = [items]
        # Convert each ItemDTO to dict for caching
        return [item.dict() for item in items]
    except ApiClientError as e:
        st.error(e.user_message)
        return []
    except Exception:
        st.error(
            "Unable to connect to backend service. Please ensure the backend server is running and reachable."
        )
        return []


def render_listings(
    items: Optional[List[dict]] = None, error_message: Optional[str] = None
) -> None:
    """
    Display listings and handle error/success feedback.
    Args:
        items: List of item dicts to render.
        error_message: Optional error message to show.
        params: Query parameters for listings API.
    """
    if error_message:
        st.error(error_message, icon="⚠️")
        return
    if items:
        for idx, item_dict in enumerate(items):
            if isinstance(item_dict, dict):
                item = ItemDTO.from_dict(item_dict)
            else:
                item = item_dict  # Already an ItemDTO
            float_display = f"{item.float_value:.6f}" if hasattr(item, "float_value") else "-"
            with st.container():
                st.markdown(
                    f"""
                    <div style='background:#23272f;padding:24px 24px 28px 24px;border-radius:14px;box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:22px; border: 2px solid #3b82f6; min-width: 280px; min-height: 120px; color: #f3f4f6;'>
                        <span style='font-size:1.4em;font-weight:bold;display:flex;align-items:center;margin-bottom:6px;'>💲 ${item.price:.2f}</span>
                        <span style='font-size:1.18em;font-weight:bold;margin-bottom:14px;'>📝 {item.name}</span>
                        <div style='width:100%;margin-bottom:10px;'>
                            <div style='display:flex;align-items:center;margin-bottom:8px;'>
                                <span style='font-size:1.05em;margin-right:8px;'>🧢 <b>Wear:</b></span>
                                <span style='font-size:1.05em;'>{item.wear}</span>
                            </div>
                            <div style='display:flex;align-items:center;margin-bottom:8px;'>
                                <span style='font-size:1.05em;margin-right:8px;'>🎖️ <b>Rarity:</b></span>
                                <span style='font-size:1.05em;'>{item.rarity}</span>
                            </div>
                            <div style='display:flex;align-items:center;'>
                                <span style='font-size:1.05em;margin-right:8px;'>🌊 <b>Float:</b></span>
                                <span style='font-size:1.05em;'>{float_display}</span>
                            </div>
                        </div>
                        <div style='margin-top:18px;width:100%;display:flex;justify-content:flex-start;'>
                            <button style='background:#3b82f6;color:#fff;border:none;padding:12px 28px;border-radius:8px;font-size:1.08em;cursor:pointer;'>View Details</button>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No listings to display. Please apply filters to fetch items.")
