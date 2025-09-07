from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from services.csfloat.client import CSFloatClient


class ItemNamesResponse(BaseModel):
    names: list[str]


router = APIRouter()
csfloat_client = CSFloatClient()


@router.get("/item-names", response_model=ItemNamesResponse)
def get_item_names(limit: int = Query(50, ge=1, le=500)):
    try:
        names = csfloat_client.fetch_item_names(limit=limit)
        return {"names": names}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Item names service unavailable: {str(e)}")
