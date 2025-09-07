from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException
from openai import AuthenticationError

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
    except AuthenticationError:
        # Map provider auth failures to 401 Unauthorized
        raise HTTPException(
            status_code=401,
            detail=(
                "Authentication with the model provider failed. Verify your API key and base URL."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get AI analysis: {str(e)}")
