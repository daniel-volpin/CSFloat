from fastapi import APIRouter, Query, HTTPException
import requests
from models import ListingQueryParams
from utils import get_api_key, logger

router = APIRouter()

# Helper to build query params dict

def build_query_params(params: ListingQueryParams):
    query = {}
    for key, value in params.dict(exclude_none=True).items():
        if isinstance(value, list):
            query[key] = ','.join(map(str, value))
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
    type: str = Query(None),
    stickers: str = Query(None)
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
        type=type,
        stickers=stickers
    )
    url = "https://csfloat.com/api/v1/listings"
    headers = {"Authorization": get_api_key()}
    query_params = build_query_params(params)
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0 and "data" in data[0]:
            return data[0]["data"]
        elif isinstance(data, dict) and "data" in data:
            return data["data"]
        else:
            return []
    except requests.RequestException as e:
        logger.error(f"Error fetching listings: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch listings from CSFloat API.")
