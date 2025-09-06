import os
from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Query

from ..models.models import ItemDTO
from ..services.llm_client import ask_about_listings

router = APIRouter()

USE_DUMMY_DATA = os.getenv("USE_DUMMY_DATA", "false").lower() in ("1", "true", "yes")


@router.get("/item-names")
def fetch_item_names_endpoint(limit: int = 50):
    # In production, disable dummy responses and return 503
    if not USE_DUMMY_DATA:
        raise HTTPException(status_code=503, detail="Item names service unavailable.")
    sample_names = ["Sample Item", "Another Item", "Cool Skin", "Rare Collectible"]
    return {"names": sample_names[:limit]}


@router.get("/listings")
def get_listings(
    limit: int = Query(10),
    sort_by: str = Query("best_deal"),
    category: int = Query(0),
    min_float: float = Query(0.0),
    max_float: float = Query(1.0),
):
    # In production, disable dummy responses and return 503
    if not USE_DUMMY_DATA:
        raise HTTPException(status_code=503, detail="Listings service unavailable.")
    sample_items = [
        ItemDTO(
            name="Sample Item",
            price=100,
            wear="Factory New",
            rarity="Rare",
            float_value=0.05,
        ),
        ItemDTO(
            name="Another Item",
            price=150,
            wear="Minimal Wear",
            rarity="Common",
            float_value=0.15,
        ),
    ]
    return {"data": sample_items[:limit]}


@router.post("/analyze")
def analyze_listings(
    question: str = Body(...),
    items: List[ItemDTO] = Body(...),
    model: Optional[str] = Body(None),
    max_items: int = Body(50),
):
    try:
        result = ask_about_listings(question, items, model, max_items)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
