from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from ...services.llm.registry import LLMModelInfo, list_models

router = APIRouter()


class LlmModelOption(BaseModel):

    label: str
    value: str  # e.g., "openai:gpt-4o-mini" or "lmstudio:qwen/qwen3-8b"


class LlmModelsResponse(BaseModel):

    models: List[LlmModelOption]


@router.get("/models", response_model=LlmModelsResponse)
def list_llm_models():
    entries: List[LLMModelInfo] = list_models()
    options: List[LlmModelOption] = [
        LlmModelOption(label=e.display, value=f"{e.provider}:{e.key}") for e in entries
    ]
    return {"models": options}
