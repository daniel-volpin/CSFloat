from fastapi import APIRouter, Query, HTTPException
import requests
router = APIRouter()
from models import ListingQueryParams
from utils import get_api_key, logger


import time
from typing import Dict, Tuple, Any
LISTINGS_CACHE: Dict[Tuple[Tuple[str, Any], ...], Dict[str, Any]] = {}
CACHE_TTL = 300  # seconds (5 minutes)

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
    paint_seed: int = Query(None),
    paint_index: int = Query(None),
    user_id: str = Query(None),
    collection: str = Query(None),
    min_price: int = Query(None),
    max_price: int = Query(None),
    market_hash_name: str = Query(None),
    item_name: str = Query(None),
    type: str = Query(None),
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
        type=type,
        stickers=stickers,
    )
    query_params = build_query_params(params)
    cache_key = tuple(sorted(query_params.items()))
    now = time.time()
    # Check cache
    cached = LISTINGS_CACHE.get(cache_key)
    if cached and now - cached['timestamp'] < CACHE_TTL:
        print(f"[CACHE] Returning cached result for params: {query_params}")
        return cached['result']

    url = "https://csfloat.com/api/v1/listings"
    headers = {"Authorization": get_api_key()}
    try:
        print(f"[DEBUG] Sending request to CSFloat API with params: {query_params}")
        response = requests.get(url, headers=headers, params=query_params)
        print(f"[DEBUG] CSFloat API response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        print(f"[DEBUG] CSFloat API response data: {str(data)[:500]}")
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
        logger.error(f"Error fetching listings: {e}")
        print(f"[DEBUG] Exception: {e}")
        raise HTTPException(
            status_code=502, detail="Failed to fetch listings from CSFloat API."
        )
