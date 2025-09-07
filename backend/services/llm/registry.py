from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import List, Literal

from ...config.settings import get_settings

Provider = Literal["openai", "lmstudio"]


@dataclass(frozen=True)
class LLMModelInfo:
    provider: Provider
    key: str
    display: str
    recommended: bool = False


_cache_lock = threading.Lock()
_cache_models: List[LLMModelInfo] | None = None
_cache_expiry: float = 0.0


def _list_lmstudio_downloaded_llms() -> List[LLMModelInfo]:
    try:
        import lmstudio as lms  # type: ignore
    except Exception:
        return []
    models: List[LLMModelInfo] = []
    try:
        for m in lms.list_downloaded_models("llm"):
            model_key = getattr(m, "model_key", None) or getattr(m, "modelKey", None)
            display = getattr(m, "display_name", None) or getattr(m, "displayName", None)
            if not model_key:
                continue
            label = f"{display or model_key} (LM Studio)"
            models.append(LLMModelInfo(provider="lmstudio", key=str(model_key), display=label))
    except Exception:
        return []
    return models


def _openai_default_model() -> LLMModelInfo:
    settings = get_settings()
    openai_default = settings.OPENAI_MODEL or "gpt-4o-mini"
    label = f"{openai_default}"
    return LLMModelInfo(provider="openai", key=str(openai_default), display=label, recommended=True)


def list_models(ttl_seconds: int = 10) -> List[LLMModelInfo]:
    global _cache_models, _cache_expiry
    now = time.time()
    with _cache_lock:
        if _cache_models is not None and now < _cache_expiry:
            return list(_cache_models)
        models: List[LLMModelInfo] = []
        lm_models = _list_lmstudio_downloaded_llms()
        if lm_models:
            models.extend(lm_models)
        models.append(_openai_default_model())
        _cache_models = models
        _cache_expiry = now + ttl_seconds
        return list(models)
