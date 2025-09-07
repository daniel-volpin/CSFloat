import os
import threading
from typing import List, Tuple

import requests
from cachetools import TTLCache

from ..models.models import ItemDTO
from .csfloat_params import normalize_listings_params

# Global cache for listings (maxsize=128, ttl=600s = 10min)
_CACHE_TTL_SECONDS = 600
_listings_cache = TTLCache(maxsize=128, ttl=_CACHE_TTL_SECONDS)
_cache_lock = threading.Lock()
_cache_hits = 0
_cache_misses = 0

CSFLOAT_API_KEY = os.getenv("CSFLOAT_API_KEY")
CSFLOAT_API_URL = os.getenv("CSFLOAT_API_URL", "https://csfloat.com/api/v1/listings")


def fetch_csfloat_listings(params: dict) -> Tuple[List[ItemDTO], str]:
    """
    Fetch listings from CSFloat with a small in-memory TTL cache.

    Returns: (items, cache_status) where cache_status is "HIT" or "MISS".
    - The cache key is computed from the normalized params actually sent to
      the upstream API to avoid returning mismatched results.
    """
    headers = {"Authorization": CSFLOAT_API_KEY} if CSFLOAT_API_KEY else {}
    # Build normalized params actually sent to upstream API
    filtered_params: dict = normalize_listings_params(params)
    # Compute a stable cache key from normalized params
    try:
        import json

        cache_key = json.dumps(filtered_params, sort_keys=True, separators=(",", ":"))
    except Exception:
        cache_key = str(sorted(filtered_params.items()))

    with _cache_lock:
        global _cache_hits, _cache_misses
        if cache_key in _listings_cache:
            _cache_hits += 1
            return _listings_cache[cache_key], "HIT"
        _cache_misses += 1
    response = requests.get(CSFLOAT_API_URL, params=filtered_params, headers=headers, timeout=10)
    response.raise_for_status()
    resp_json = response.json()
    listings = resp_json.get("data", [])
    if not isinstance(listings, list):
        raise RuntimeError(f"CSFloat API 'data' field is not a list. Response: {resp_json}")
    items: List[ItemDTO] = []
    for listing in listings:
        item = listing.get("item", {})
        rarity_raw = item.get("rarity")
        rarity_label = None
        if isinstance(rarity_raw, int):
            rarity_label = {
                1: "Common",
                2: "Uncommon",
                3: "Rare",
                4: "Mythical",
                5: "Legendary",
                6: "Ancient",
                7: "Immortal",
            }.get(rarity_raw)
        elif isinstance(rarity_raw, str):
            rarity_label = rarity_raw
        items.append(
            ItemDTO(
                name=item.get("item_name"),
                price=listing.get("price"),
                wear=item.get("wear_name"),
                rarity=rarity_label,
                float_value=item.get("float_value"),
            )
        )
    with _cache_lock:
        _listings_cache[cache_key] = items
    return items, "MISS"


# Utility functions for cache inspection/invalidation
def get_cache_stats():
    with _cache_lock:
        return {
            "size": len(_listings_cache),
            "keys": list(_listings_cache.keys()),
            "hits": _cache_hits,
            "misses": _cache_misses,
            "ttl_seconds": _CACHE_TTL_SECONDS,
        }


def invalidate_cache():
    with _cache_lock:
        _listings_cache.clear()


def fetch_csfloat_item_names(limit: int = 50) -> List[str]:
    url = os.getenv("CSFLOAT_API_ITEM_NAMES_URL", "https://api.csfloat.com/api/v1/item-names")
    response = requests.get(url, params={"limit": limit}, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("names", [])
