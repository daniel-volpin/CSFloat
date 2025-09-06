import time
from .models import ListingQueryParams
from typing import Dict, Tuple, Any
from fastapi import APIRouter, Query, HTTPException
from .utils import get_api_key, logger
import requests

router = APIRouter()


LISTINGS_CACHE: Dict[Tuple[Tuple[str, Any], ...], Dict[str, Any]] = {}
CACHE_TTL = 300  # seconds (5 minutes)
# Lightweight cache for item names endpoint
NAMES_CACHE: Dict[int, Dict[str, Any]] = {}

# Helper to build query params dict


def build_query_params(params: ListingQueryParams):
    query = {}
    for key, value in params.dict(exclude_none=True).items():
        if isinstance(value, list):
            query[key] = ",".join(map(str, value))
        else:
            query[key] = value
    return query


@router.get("/listings")
def get_listings(
    cursor: str = Query(None),
    limit: int = Query(50, ge=1, le=50),
    sort_by: str = Query("best_deal"),
    category: int = Query(0),
    def_index: list[int] = Query(None),
    min_float: float = Query(None),
    max_float: float = Query(None),
    rarity: str = Query(None),
    paint_seed: list[int] | None = Query(None),
    paint_index: int = Query(None),
    user_id: str = Query(None),
    collection: str = Query(None),
    min_price: int = Query(None),
    max_price: int = Query(None),
    market_hash_name: str = Query(None),
    item_name: str = Query(None),
    type_: str = Query(None, alias="type"),
    stickers: str = Query(None),
):
    params = ListingQueryParams(
        cursor=cursor,
        limit=limit,
        sort_by=sort_by,
        category=category,
        def_index=def_index,
        min_float=min_float,
        max_float=max_float,
        rarity=rarity,
        paint_seed=paint_seed,
        paint_index=paint_index,
        user_id=user_id,
        collection=collection,
        min_price=min_price,
        max_price=max_price,
        market_hash_name=market_hash_name,
        item_name=item_name,
        type=type_,
        stickers=stickers,
    )
    query_params = build_query_params(params)
    cache_key = tuple(sorted(query_params.items()))
    now = time.time()
    # Check cache
    cached = LISTINGS_CACHE.get(cache_key)
    if cached and now - cached["timestamp"] < CACHE_TTL:
        logger.debug(f"[CACHE] Returning cached result for params: {query_params}")
        return cached["result"]

    url = "https://csfloat.com/api/v1/listings"
    headers = {"Authorization": get_api_key()}
    try:
        logger.debug(f"Sending request to CSFloat API with params: {query_params}")
        response = requests.get(
            url, headers=headers, params=query_params, timeout=(3.05, 10)
        )
        logger.debug(f"CSFloat API response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        logger.debug(f"CSFloat API response data: {str(data)[:500]}")
        # Support both list and dict response formats
        if isinstance(data, list) and len(data) > 0 and "data" in data[0]:
            result = {"data": data[0]["data"], "cursor": data[0].get("cursor")}
        elif isinstance(data, dict) and "data" in data:
            result = {"data": data["data"], "cursor": data.get("cursor")}
        else:
            result = {"data": [], "cursor": None}
        # Store in cache
        LISTINGS_CACHE[cache_key] = {"result": result, "timestamp": now}
        return result
    except requests.RequestException as e:
        logger.exception(f"Error fetching listings: {e}")
        raise HTTPException(
            status_code=502, detail="Failed to fetch listings from CSFloat API."
        )


@router.get("/item-names")
def get_item_names(limit: int = Query(50, ge=1, le=200)):
    """Return a cached, alphabetized list of item names from CSFloat listings."""
    now = time.time()
    cached = NAMES_CACHE.get(limit)
    if cached and now - cached["timestamp"] < CACHE_TTL:
        logger.debug(f"[CACHE] Returning cached item names (limit={limit})")
        return {"names": cached["result"]}

    url = "https://csfloat.com/api/v1/listings"
    headers = {"Authorization": get_api_key()}
    params = {"limit": limit}
    try:
        logger.debug(f"Fetching item names with params: {params}")
        response = requests.get(url, headers=headers, params=params, timeout=(3.05, 10))
        response.raise_for_status()
        data = response.json()
        # Normalize to list of entries
        if isinstance(data, dict) and "data" in data:
            entries = data["data"]
        elif isinstance(data, list) and len(data) > 0 and "data" in data[0]:
            entries = data[0]["data"]
        else:
            entries = []
        names = sorted(
            {
                (entry.get("item") or {}).get("name")
                or entry.get("item_name")
                for entry in entries
                if ((entry.get("item") or {}).get("name") or entry.get("item_name"))
            }
        )
        NAMES_CACHE[limit] = {"result": names, "timestamp": now}
        return {"names": names}
    except requests.RequestException as e:
        logger.exception(f"Error fetching item names: {e}")
        raise HTTPException(
            status_code=502, detail="Failed to fetch item names from CSFloat API."
        )
