from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...core.exceptions import BackendError, UpstreamServiceError, ValidationError
from ...services.llm.registry import LLMModelInfo, list_models

router = APIRouter()


class LlmModelOption(BaseModel):

    label: str
    value: str  # e.g., "openai:gpt-4o-mini" or "lmstudio:qwen/qwen3-8b"


class LlmModelsResponse(BaseModel):

    models: List[LlmModelOption]


@router.get("/models", response_model=LlmModelsResponse)
def list_llm_models() -> LlmModelsResponse:
    try:
        entries: List[LLMModelInfo] = list_models()
        options: List[LlmModelOption] = [
            LlmModelOption(label=e.display, value=f"{e.provider}:{e.key}") for e in entries
        ]
        return LlmModelsResponse(models=options)
    except UpstreamServiceError as e:
        raise HTTPException(
            status_code=503, detail=f"Upstream LLM model service unavailable: {str(e)}"
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except BackendError as e:
        raise HTTPException(status_code=500, detail=f"Internal backend error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
