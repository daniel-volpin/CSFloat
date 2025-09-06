import requests
import streamlit as st
from models import ItemDTO
from config import LISTINGS_ENDPOINT

import time


@st.cache_data(show_spinner=False)
def fetch_listings(params):
    start = time.time()
    response = requests.get(LISTINGS_ENDPOINT, params=params)
    response.raise_for_status()
    data = response.json()
    listings = []
    for entry in data:
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
