from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..services.csfloat_client import fetch_csfloat_item_names


class ItemNamesResponse(BaseModel):
    names: list[str]


router = APIRouter()


@router.get("/item-names", response_model=ItemNamesResponse)
def get_item_names(limit: int = Query(50, ge=1, le=500)):
    try:
        names = fetch_csfloat_item_names(limit=limit)
        return {"names": names}
    except Exception as e:
        # Upstream unavailable or invalid response
        raise HTTPException(status_code=503, detail=f"Item names service unavailable: {str(e)}")
