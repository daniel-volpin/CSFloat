import requests
import streamlit as st
from models import ItemDTO
from config import LISTINGS_ENDPOINT

import time


@st.cache_data(show_spinner=False)
def fetch_listings(params):
    start = time.time()
    try:
        response = requests.get(LISTINGS_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict) or "data" not in data:
            import streamlit as st

            st.error(f"Unexpected response from backend: {data}")
            return []
        listings = []
        for entry in data["data"]:
            merged = {}
            if "item" in entry and isinstance(entry["item"], dict):
                merged.update(entry["item"])
            merged.update({k: v for k, v in entry.items() if k != "item"})
            listings.append(ItemDTO.from_dict(merged))
        elapsed = time.time() - start
        if elapsed < 0.1:
            print("[Cache] Using cached listings!")
        else:
            print(f"[Cache] Fetching listings from API... ({elapsed:.2f}s)")
        return listings
    except requests.HTTPError as e:
        code = e.response.status_code if e.response else None
        error_map = {
            400: "Bad Request: Your request is invalid.",
            401: "Unauthorized: Your API key is wrong.",
            403: "Forbidden: The item is restricted.",
            404: "Not Found: The item could not be found.",
            405: "Method Not Allowed: Invalid method.",
            406: "Not Acceptable: Requested format isn't JSON.",
            410: "Gone: The item has been removed.",
            418: "I'm a teapot.",
            429: "Too Many Requests: Slow down!",
            500: "Internal Server Error: Try again later.",
            503: "Service Unavailable: Maintenance in progress.",
        }
        import streamlit as st

        st.error(
            error_map.get(code if code is not None else -1, f"Unexpected error: {code}")
        )
        return []
    except Exception as e:
        import streamlit as st

        st.error(f"Unexpected error: {e}")
        return []
