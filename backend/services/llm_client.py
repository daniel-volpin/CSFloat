import os
from typing import List, Optional
from ..models.models import ItemDTO
from .openai_client import OpenAIClient


def _build_listings_digest(items: List[ItemDTO], max_items: int = 50) -> str:
    lines = []
    for i, it in enumerate(items[: max_items if max_items > 0 else 50], start=1):
        price_str = f"${(it.price or 0) / 100:.2f}" if it.price is not None else "N/A"
        wear = it.wear or "N/A"
        rarity = it.rarity or "N/A"
        fl = f"{it.float_value:.6f}" if it.float_value is not None else "N/A"
        name = it.name or "Unknown"
        lines.append(f"{i}. {name} | {price_str} | wear={wear} | rarity={rarity} | float={fl}")
    return "\n".join(lines)


def ask_about_listings(
    question: str,
    items: List[ItemDTO],
    model: Optional[str] = None,
    max_items: int = 50,
) -> str:
    if not items:
        return "No listings are loaded. Adjust filters and try again."
    client = OpenAIClient()
    chosen_model = model or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
    reduced_items = max_items
    if "gpt-5-nano" in chosen_model.lower():
        reduced_items = min(max_items, 10)
    digest = _build_listings_digest(items, max_items=reduced_items)
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
    try:
        resp = client.chat(model=chosen_model, messages=messages, temperature=0.2, max_tokens=300)
        return resp
    except Exception as e:
        return f"LLM request failed: {str(e)}"
