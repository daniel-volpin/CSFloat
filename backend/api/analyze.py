from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException

from ..models.models import ItemDTO
from ..services.llm_client import ask_about_listings

router = APIRouter()


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
