import os
import threading
from typing import List

import requests
from cachetools import TTLCache

from ..models.models import ItemDTO

# Global cache for listings (maxsize=128, ttl=600s = 10min)
_listings_cache = TTLCache(maxsize=128, ttl=600)
_cache_lock = threading.Lock()

CSFLOAT_API_KEY = os.getenv("CSFLOAT_API_KEY")
CSFLOAT_API_URL = os.getenv("CSFLOAT_API_URL", "https://csfloat.com/api/v1/listings")


def fetch_csfloat_listings(params: dict) -> List[ItemDTO]:
    """
    Fetch listings from CSFloat with a small in-memory TTL cache.

    Notes on price units:
    - The frontend sends price filters in dollars (float), which are converted
      to cents here for the upstream API.
    - The cache key is computed from the normalized params actually sent to
      the upstream API to avoid returning mismatched results.
    """
    headers = {"Authorization": CSFLOAT_API_KEY} if CSFLOAT_API_KEY else {}
    # Build normalized params actually sent to upstream API
    filtered_params: dict = {}
    for k, v in params.items():
        if v is None or v == "" or (isinstance(v, (list, dict)) and not v):
            continue
        if k in ["min_price", "max_price"]:
            # Convert dollars -> cents for upstream API
            if isinstance(v, (int, float)) or (
                isinstance(v, str) and v.replace(".", "", 1).isdigit()
            ):
                try:
                    cents = int(float(v) * 100)
                except Exception:
                    cents = None
                if cents is not None and cents >= 0:
                    filtered_params[k] = cents
        else:
            filtered_params[k] = v
    # Compute a stable cache key from normalized params
    try:
        import json

        cache_key = json.dumps(filtered_params, sort_keys=True, separators=(",", ":"))
    except Exception:
        cache_key = str(sorted(filtered_params.items()))

    with _cache_lock:
        if cache_key in _listings_cache:
            return _listings_cache[cache_key]
    response = requests.get(CSFLOAT_API_URL, params=filtered_params, headers=headers, timeout=10)
    response.raise_for_status()
    resp_json = response.json()
    listings = resp_json.get("data", [])
    if not isinstance(listings, list):
        raise RuntimeError(f"CSFloat API 'data' field is not a list. Response: {resp_json}")
    items = []
    for listing in listings:
        item = listing.get("item", {})
        items.append(
            ItemDTO(
                name=item.get("item_name"),
                price=listing.get("price"),
                wear=item.get("wear_name"),
                rarity=item.get("rarity"),
                float_value=item.get("float_value"),
            )
        )
    with _cache_lock:
        _listings_cache[cache_key] = items
    return items


# Utility functions for cache inspection/invalidation
def get_cache_contents():
    with _cache_lock:
        return dict(_listings_cache)


def invalidate_cache():
    with _cache_lock:
        _listings_cache.clear()


def fetch_csfloat_item_names(limit: int = 50) -> List[str]:
    url = os.getenv("CSFLOAT_API_ITEM_NAMES_URL", "https://api.csfloat.com/api/v1/item-names")
    response = requests.get(url, params={"limit": limit}, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("names", [])
