from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ...core.exceptions import BackendError, UpstreamServiceError, ValidationError
from ...services.csfloat.client import CSFloatClient


class ItemNamesResponse(BaseModel):
    names: list[str]


router = APIRouter()
csfloat_client = CSFloatClient()


@router.get("/", response_model=ItemNamesResponse)
def get_item_names(limit: int = Query(50, ge=1, le=500)) -> ItemNamesResponse:
    try:
        names = csfloat_client.fetch_item_names(limit=limit)
        return ItemNamesResponse(names=names)
    except (UpstreamServiceError, RuntimeError) as e:
        raise HTTPException(
            status_code=503, detail=f"Upstream item names service unavailable: {str(e)}"
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except BackendError as e:
        raise HTTPException(status_code=500, detail=f"Internal backend error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
