import json
import os
import threading
from typing import List, Optional, Tuple

import httpx
from cachetools import TTLCache

# Optional HTTP/2 support detection for httpx
try:

    _HAS_H2 = True
except Exception:  # pragma: no cover - optional dependency
    _HAS_H2 = False

from ..config.settings import get_settings
from ..models.models import ItemDTO
from .csfloat_params import normalize_listings_params

_settings = get_settings()

# Global cache for listings
_listings_cache: TTLCache = TTLCache(
    maxsize=_settings.CACHE_MAXSIZE, ttl=_settings.CACHE_TTL_SECONDS
)
_cache_lock = threading.Lock()
_inflight: dict[str, threading.Event] = {}
_cache_hits = 0
_cache_misses = 0

CSFLOAT_API_KEY = _settings.CSFLOAT_API_KEY or os.getenv("CSFLOAT_API_KEY")
CSFLOAT_API_URL = _settings.CSFLOAT_API_URL or os.getenv(
    "CSFLOAT_API_URL", "https://csfloat.com/api/v1/listings"
)

# Shared HTTP client with pooling and optional HTTP/2
_http2_enabled = bool(_settings.HTTP2_ENABLED) and _HAS_H2

_http_client: Optional[httpx.Client] = None


def _create_default_client() -> httpx.Client:
    return httpx.Client(
        http2=_http2_enabled,
        timeout=httpx.Timeout(
            connect=float(_settings.REQUEST_CONNECT_TIMEOUT),
            read=float(_settings.REQUEST_READ_TIMEOUT),
            write=float(_settings.REQUEST_READ_TIMEOUT),
            pool=float(_settings.HTTPX_POOL_TIMEOUT),
        ),
        limits=httpx.Limits(
            max_keepalive_connections=int(_settings.HTTPX_MAX_KEEPALIVE),
            max_connections=int(_settings.HTTPX_MAX_CONNECTIONS),
        ),
    )


def set_http_client(client: httpx.Client) -> None:
    global _http_client
    _http_client = client


def _get_http_client() -> httpx.Client:
    global _http_client
    if _http_client is None:
        _http_client = _create_default_client()
    return _http_client


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
        cache_key = json.dumps(filtered_params, sort_keys=True, separators=(",", ":"))
    except Exception:
        cache_key = str(sorted(filtered_params.items()))

    # Single-flight: avoid dogpile
    wait_seconds = float(_settings.SINGLE_FLIGHT_WAIT_SECONDS)
    while True:
        with _cache_lock:
            global _cache_hits, _cache_misses
            if cache_key in _listings_cache:
                _cache_hits += 1
                return _listings_cache[cache_key], "HIT"
            ev = _inflight.get(cache_key)
            if ev is None:
                ev = threading.Event()
                _inflight[cache_key] = ev
                # This caller becomes the fetcher
                _cache_misses += 1
                break
        # Another fetch already in-flight; wait briefly then re-check
        ev.wait(timeout=wait_seconds)
        # loop to re-check cache or become fetcher if prior failed

    # Perform upstream request (this is the single fetcher for the key)
    try:
        client = _get_http_client()
        response = client.get(CSFLOAT_API_URL, params=filtered_params, headers=headers)
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
    finally:
        # Always release inflight waiters even on error
        with _cache_lock:
            ev2 = _inflight.pop(cache_key, None)
            if ev2 is not None:
                ev2.set()


# Utility functions for cache inspection/invalidation
def get_cache_stats():
    with _cache_lock:
        return {
            "size": len(_listings_cache),
            "keys": list(_listings_cache.keys()),
            "hits": _cache_hits,
            "misses": _cache_misses,
            "ttl_seconds": _settings.CACHE_TTL_SECONDS,
        }


def invalidate_cache():
    with _cache_lock:
        _listings_cache.clear()
        # Clear inflight events as well
        for ev in _inflight.values():
            ev.set()
        _inflight.clear()


def fetch_csfloat_item_names(limit: int = 50) -> List[str]:
    url = os.getenv("CSFLOAT_API_ITEM_NAMES_URL", _settings.CSFLOAT_ITEM_NAMES_URL)
    client = _get_http_client()
    response = client.get(url, params={"limit": limit})
    response.raise_for_status()
    data = response.json()
    return data.get("names", [])
