from __future__ import annotations

import os
from typing import List, Optional

from ...config.settings import get_settings
from ...models.models import ItemDTO
from .formatting import build_listings_digest
from .openai_client import OpenAIClient
from .router import choose_provider_and_model, get_provider


def ask_about_listings(
    question: str,
    items: List[ItemDTO],
    model: Optional[str] = None,
    max_items: int = 50,
) -> str:
    if not items:
        return "No listings are loaded. Adjust filters and try again."

    settings = get_settings()
    provider_env = os.getenv("LLM_PROVIDER") or settings.LLM_PROVIDER or "openai"
    provider, chosen_model = choose_provider_and_model(model, provider_env)

    reduced_items = max_items
    if "gpt-5-nano" in chosen_model.lower():
        reduced_items = min(max_items, 10)

    digest = build_listings_digest(items, max_items=reduced_items)
    system = (
        "You analyze CS:GO marketplace listings for investing. "
        "Be precise and concise. Prefer numeric comparisons (price, float). "
        "If the question is ambiguous, ask for clarification briefly. "
        "Only use the provided listings; do not assume external pricing."
    )
    user = (
        "Here are the current listings (index. name | price | wear | rarity | float):\n\n"
        f"{digest}\n\n"
        f"Question: {question}\n\n"
        "Instructions: If recommending items, reference them by index and name, "
        "explain the rationale (e.g., low float, rarity, price), and suggest 3–5 options at most."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    if provider == "lmstudio":
        try:
            client = get_provider(provider)
            return client.chat(
                model=chosen_model, messages=messages, temperature=0.2, max_tokens=300
            )
        except Exception:
            pass

    client = OpenAIClient()
    return client.chat(model=chosen_model, messages=messages, temperature=0.2, max_tokens=300)
