from __future__ import annotations

import re
from typing import Any, Optional


class LMStudioClient:
    """
    Thin wrapper around the LM Studio Python SDK for simple chat-style prompts.

    Expects the LM Studio app to be running locally with the developer API enabled.
    Always relies on the SDK to auto‑detect the local server; no explicit host is required.
    """

    def __init__(self, api_host: Optional[str] = None):
        try:  # pragma: no cover - optional dependency
            import lmstudio as _lms  # type: ignore
        except Exception:
            raise RuntimeError(
                "lmstudio package is not installed. Run `pip install lmstudio` to enable."
            )
        self._lms: Any = _lms
        # Always rely on SDK auto‑detect for local server (ignore api_host)
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
        # Build LM Studio chat object from OpenAI‑style messages
        chat = self._lms.Chat.from_history({"messages": messages})
        llm = self._lms.llm(model)
        text: str = ""
        try:
            cfg: dict[str, Any] = {
                "temperature": float(temperature),
                # Hide chain-of-thought from capable models (e.g., <think>...</think>)
                # Use SDK reasoning parsing so `content` returns the final answer section.
                "reasoningParsing": {
                    "enabled": True,
                    "startString": "<think>",
                    "endString": "</think>",
                },
            }
            if int(max_tokens) > 0:
                cfg["maxTokens"] = int(max_tokens)
            if stream:
                # Aggregate streamed tokens to a final string
                chunks: list[str] = []
                for fragment in llm.respond_stream(history=chat, config=cfg):
                    # fragment is LlmPredictionFragment or message events; only collect text
                    if getattr(fragment, "content", None):
                        chunks.append(fragment.content)
                text = "".join(chunks)
            else:
                result = llm.respond(history=chat, config=cfg)
                text = result.content or ""
        except Exception as e:  # Surface a clean error up the stack
            raise RuntimeError(f"LM Studio request failed: {e}")
        # PredictionResult.content contains the assistant text (may still include tags on some models)
        # Prefer the final channel content if special tags are present
        final_token = "<|channel|>final<|message|>"
        if final_token in text:
            text = text.split(final_token, 1)[1]
        if "<think>" in text and "</think>" in text:
            # Fallback sanitize in case parsing doesn't strip it in current SDK/runtime
            text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
        # Remove any residual special tag markers like <|channel|>, <|message|>, <|start|>, <|end|>
        text = re.sub(r"<\|[^>]+\|>", "", text)
        text = text.strip()
        return text or "(No response)"
