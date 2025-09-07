from __future__ import annotations

import os
from typing import Tuple

from ...config.settings import get_settings
from .lmstudio_client import LMStudioClient
from .openai_client import OpenAIClient
from .registry import list_models
from .types import ChatProvider


def choose_provider_and_model(model: str | None, provider_env: str | None) -> Tuple[str, str]:
    settings = get_settings()
    provider = (provider_env or settings.LLM_PROVIDER or "openai").strip().lower()
    chosen_model = (model or "").strip()

    if chosen_model.lower().startswith("lmstudio:"):
        provider = "lmstudio"
        chosen_model = chosen_model.split(":", 1)[1].strip()
    elif chosen_model.lower().startswith("openai:"):
        provider = "openai"
        chosen_model = chosen_model.split(":", 1)[1].strip()

    if not chosen_model:
        try:
            available = list_models()
            first = available[0] if available else None
            if first and first.provider == "lmstudio":
                provider = "lmstudio"
                chosen_model = (
                    settings.LMSTUDIO_MODEL
                    or os.getenv("LMSTUDIO_MODEL")
                    or first.key
                    or "qwen/qwen3-8b"
                )
            else:
                provider = "openai"
                chosen_model = settings.OPENAI_MODEL or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
        except Exception:
            provider = "openai"
            chosen_model = settings.OPENAI_MODEL or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"

    return provider, chosen_model


def get_provider(provider: str) -> ChatProvider:
    if provider == "lmstudio":
        return LMStudioClient()
    return OpenAIClient()
