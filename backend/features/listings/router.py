from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ...models.models import ItemDTO
from ...services.csfloat.client import CSFloatClient


class ListingsResponse(BaseModel):
    data: List[ItemDTO]
    meta: Optional[dict] = None


router = APIRouter()
csfloat_client = CSFloatClient()


@router.get("/", response_model=ListingsResponse)
def get_listings(
    limit: int = Query(10, ge=1, le=50),
    sort_by: str = Query("best_deal"),
    category: int = Query(0),
    min_float: float = Query(0.0),
    max_float: float = Query(1.0),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    cursor: Optional[str] = Query(None),
    def_index: Optional[List[int]] = Query(None),
    rarity: Optional[int] = Query(None),
    paint_seed: Optional[List[int]] = Query(None),
    paint_index: Optional[int] = Query(None),
    user_id: Optional[str] = Query(None),
    collection: Optional[str] = Query(None),
    market_hash_name: Optional[str] = Query(None),
    item_name: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    stickers: Optional[str] = Query(None),
):
    try:
        params = {
            "limit": limit,
            "sort_by": sort_by,
            "category": category,
            "min_float": min_float,
            "max_float": max_float,
            "min_price": min_price,
            "max_price": max_price,
            "cursor": cursor,
            "def_index": def_index,
            "rarity": rarity,
            "paint_seed": paint_seed,
            "paint_index": paint_index,
            "user_id": user_id,
            "collection": collection,
            "market_hash_name": market_hash_name,
            "item_name": item_name,
            "type": type,
            "stickers": stickers,
        }
        items, cache_status = csfloat_client.fetch_listings(params)
        return {"data": items, "meta": {"cache": cache_status}}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Listings service unavailable: {str(e)}")
