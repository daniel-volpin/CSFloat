from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException
from openai import AuthenticationError
from pydantic import BaseModel

from ...core.exceptions import BackendError, UpstreamServiceError, ValidationError
from ...models.item_dto import ItemDTO
from ...services.llm.client import LLMClient

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
def analyze_listings(payload: AnalyzeRequest = Body(...)) -> AnalyzeResponse:
    try:
        result = llm_client.ask_about_listings(
            payload.question, payload.items, payload.model, payload.max_items
        )
        return AnalyzeResponse(result=result)
    except AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail=(
                "Authentication with the model provider failed. Verify your API key and base URL."
            ),
        )
    except UpstreamServiceError as e:
        raise HTTPException(status_code=503, detail=f"Upstream model service unavailable: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except BackendError as e:
        raise HTTPException(status_code=500, detail=f"Internal backend error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
