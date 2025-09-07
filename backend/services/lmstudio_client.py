from __future__ import annotations

import re
from typing import Any, Optional


class LMStudioClient:
    """Minimal LM Studio chat wrapper.

    Auto-detects the local server; requires the LM Studio app with Developer API enabled.
    """

    def __init__(self, api_host: Optional[str] = None):
        try:  # pragma: no cover - optional dependency
            import lmstudio as _lms  # type: ignore
        except Exception:
            raise RuntimeError(
                "lmstudio package is not installed. Run `pip install lmstudio` to enable."
            )
        self._lms: Any = _lms
        self.client = self._lms.get_default_client()

    def chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        *,
        temperature: float = 0.2,
        max_tokens: int = 300,
        stream: bool = False,
    ) -> str:
        chat = self._lms.Chat.from_history({"messages": messages})
        llm = self._lms.llm(model)
        text: str = ""
        try:
            cfg: dict[str, Any] = {
                "temperature": float(temperature),
                "reasoningParsing": {
                    "enabled": True,
                    "startString": "<think>",
                    "endString": "</think>",
                },
            }
            if int(max_tokens) > 0:
                cfg["maxTokens"] = int(max_tokens)
            if stream:
                chunks: list[str] = []
                for fragment in llm.respond_stream(history=chat, config=cfg):
                    if getattr(fragment, "content", None):
                        chunks.append(fragment.content)
                text = "".join(chunks)
            else:
                result = llm.respond(history=chat, config=cfg)
                text = result.content or ""
        except Exception as e:
            raise RuntimeError(f"LM Studio request failed: {e}")
        final_token = "<|channel|>final<|message|>"
        if final_token in text:
            text = text.split(final_token, 1)[1]
        if "<think>" in text and "</think>" in text:
            text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
        text = re.sub(r"<\|[^>]+\|>", "", text)
        text = text.strip()
        return text or "(No response)"
