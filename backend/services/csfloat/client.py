import hashlib
import json
import logging
import os
import threading
import time
from typing import Optional, Tuple

import httpx
from cachetools import TTLCache

try:
    import h2  # type: ignore  # noqa: F401

    _HAS_H2 = True
except Exception:  # pragma: no cover - optional dependency
    _HAS_H2 = False

from ...config.settings import get_settings
from .params import normalize_listings_params

_settings = get_settings()


class CSFloatClient:
    def __init__(self):
        self.logger = logging.getLogger("csfloat.client")
        self._settings = get_settings()
        self._listings_cache: TTLCache = TTLCache(
            maxsize=self._settings.CACHE_MAXSIZE, ttl=self._settings.CACHE_TTL_SECONDS
        )
        self._cache_lock = threading.Lock()
        self._inflight: dict[str, threading.Event] = {}
        self._cache_hits = 0
        self._cache_misses = 0
        self.api_key = self._settings.CSFLOAT_API_KEY or os.getenv("CSFLOAT_API_KEY")
        self.api_url = self._settings.CSFLOAT_API_URL or os.getenv(
            "CSFLOAT_API_URL", "https://csfloat.com/api/v1/listings"
        )
        self._http2_enabled = bool(self._settings.HTTP2_ENABLED) and _HAS_H2
        self._http_client: Optional[httpx.Client] = None

    def _create_default_client(self) -> httpx.Client:
        return httpx.Client(
            http2=self._http2_enabled,
            timeout=httpx.Timeout(
                connect=float(self._settings.REQUEST_CONNECT_TIMEOUT),
                read=float(self._settings.REQUEST_READ_TIMEOUT),
                write=float(self._settings.REQUEST_READ_TIMEOUT),
                pool=float(self._settings.HTTPX_POOL_TIMEOUT),
            ),
            limits=httpx.Limits(
                max_keepalive_connections=int(self._settings.HTTPX_MAX_KEEPALIVE),
                max_connections=int(self._settings.HTTPX_MAX_CONNECTIONS),
            ),
        )

    def set_http_client(self, client: httpx.Client) -> None:
        self._http_client = client

    def _get_http_client(self) -> httpx.Client:
        if self._http_client is None:
            self._http_client = self._create_default_client()
        return self._http_client

    def fetch_listings(self, params: dict) -> Tuple[list, str]:
        """Fetch listings with a small in-memory TTL cache. Returns (items, cache_status) where cache_status is "HIT" or "MISS"."""
        headers = {"Authorization": self.api_key} if self.api_key else {}
        filtered_params: dict = normalize_listings_params(params)
        try:
            cache_key = json.dumps(filtered_params, sort_keys=True, separators=(",", ":"))
        except Exception:
            cache_key = str(sorted(filtered_params.items()))
        key_id = hashlib.sha1(cache_key.encode("utf-8")).hexdigest()[:8]

        wait_seconds = float(self._settings.SINGLE_FLIGHT_WAIT_SECONDS)
        while True:
            with self._cache_lock:
                if cache_key in self._listings_cache:
                    self._cache_hits += 1
                    self.logger.info(
                        json.dumps(
                            {
                                "event": "cache_hit",
                                "key": key_id,
                                "hits": self._cache_hits,
                                "misses": self._cache_misses,
                            }
                        )
                    )
                    return self._listings_cache[cache_key], "HIT"
                ev = self._inflight.get(cache_key)
                if ev is None:
                    ev = threading.Event()
                    self._inflight[cache_key] = ev
                    self._cache_misses += 1
                    self.logger.info(
                        json.dumps(
                            {
                                "event": "cache_miss_leader",
                                "key": key_id,
                                "hits": self._cache_hits,
                                "misses": self._cache_misses,
                            }
                        )
                    )
                    break
            self.logger.info(
                json.dumps({"event": "cache_wait", "key": key_id, "wait_seconds": wait_seconds})
            )
            ev.wait(timeout=wait_seconds)

        start = time.perf_counter()
        try:
            client = self._get_http_client()
            response = client.get(self.api_url, params=filtered_params, headers=headers)
            response.raise_for_status()
            resp_json = response.json()
            listings = resp_json.get("data", [])
            if not isinstance(listings, list):
                raise RuntimeError(f"CSFloat API 'data' field is not a list. Response: {resp_json}")
            items = []
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
                    {
                        "name": item.get("item_name"),
                        "price": listing.get("price"),
                        "wear": item.get("wear_name"),
                        "rarity": rarity_label,
                        "float_value": item.get("float_value"),
                    }
                )
            duration_ms = int((time.perf_counter() - start) * 1000)
            self.logger.info(
                json.dumps(
                    {
                        "event": "fetch_ok",
                        "key": key_id,
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                        "items": len(items),
                    }
                )
            )
            with self._cache_lock:
                self._listings_cache[cache_key] = items
            return items, "MISS"
        except Exception as e:
            duration_ms = int((time.perf_counter() - start) * 1000)
            self.logger.error(
                json.dumps(
                    {
                        "event": "fetch_error",
                        "key": key_id,
                        "error": str(e),
                        "duration_ms": duration_ms,
                    }
                )
            )
            raise
        finally:
            with self._cache_lock:
                ev2 = self._inflight.pop(cache_key, None)
                if ev2 is not None:
                    ev2.set()

    def get_cache_stats(self):
        with self._cache_lock:
            return {
                "size": len(self._listings_cache),
                "keys": list(self._listings_cache.keys()),
                "hits": self._cache_hits,
                "misses": self._cache_misses,
                "ttl_seconds": self._settings.CACHE_TTL_SECONDS,
            }

    def invalidate_cache(self):
        with self._cache_lock:
            self._listings_cache.clear()
            for ev in self._inflight.values():
                ev.set()
            self._inflight.clear()

    def fetch_item_names(self, limit: int = 50) -> list:
        """Fetch item names from CSFloat item-names endpoint."""
        url = self._settings.CSFLOAT_ITEM_NAMES_URL
        headers = {"Authorization": self.api_key} if self.api_key else {}
        client = self._get_http_client()
        response = client.get(url, params={"limit": limit}, headers=headers)
        response.raise_for_status()
        data = response.json()
        names = data.get("names", [])
        return names if isinstance(names, list) else []
