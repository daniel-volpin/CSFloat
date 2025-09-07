from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Query

from ..models.models import ItemDTO
from ..services.csfloat_client import fetch_csfloat_listings
from ..services.llm_client import ask_about_listings

router = APIRouter()


@router.get("/listings")
def get_listings(
    limit: int = Query(10, ge=1, le=50),
    sort_by: str = Query("best_deal"),
    category: int = Query(0),
    min_float: float = Query(0.0),
    max_float: float = Query(1.0),
    # Prices are provided in dollars by the frontend; conversion to cents happens downstream.
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
):
    try:
        params = {
            "limit": limit,
            "sort_by": sort_by,
            "category": category,
            "min_float": min_float,
            "max_float": max_float,
        }
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        items = fetch_csfloat_listings(params)
        return {"data": items}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Listings service unavailable: {str(e)}")


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
