from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException
from openai import AuthenticationError
from pydantic import BaseModel

from ..models.models import ItemDTO
from ..services.llm_client import ask_about_listings

router = APIRouter()


class AnalyzeRequest(BaseModel):
    question: str
    items: List[ItemDTO]
    model: Optional[str] = None
    max_items: int = 50


class AnalyzeResponse(BaseModel):
    result: str


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_listings(payload: AnalyzeRequest = Body(...)):
    try:
        result = ask_about_listings(
            payload.question, payload.items, payload.model, payload.max_items
        )
        return {"result": result}
    except AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail=(
                "Authentication with the model provider failed. Verify your API key and base URL."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get AI analysis: {str(e)}")
