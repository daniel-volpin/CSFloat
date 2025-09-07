from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException
from models.models import ItemDTO
from openai import AuthenticationError
from pydantic import BaseModel
from services.llm.client import LLMClient

router = APIRouter()
llm_client = LLMClient()


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
        result = llm_client.ask_about_listings(
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
