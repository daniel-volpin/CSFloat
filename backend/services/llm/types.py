from __future__ import annotations

from typing import Any, Protocol


class ChatProvider(Protocol):
    def chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
        temperature: float = 0.2,
        max_tokens: int = 300,
    ) -> str:  # pragma: no cover - protocol definition
        ...
