from __future__ import annotations

from typing import List

from ...models.models import ItemDTO


def build_listings_digest(items: List[ItemDTO], max_items: int = 50) -> str:
    lines: list[str] = []
    limit = max_items if max_items > 0 else 50
    for i, it in enumerate(items[:limit], start=1):
        price_str = f"${(it.price or 0) / 100:.2f}" if it.price is not None else "N/A"
        wear = it.wear or "N/A"
        rarity = it.rarity or "N/A"
        fl = f"{it.float_value:.6f}" if it.float_value is not None else "N/A"
        name = it.name or "Unknown"
        lines.append(f"{i}. {name} | {price_str} | wear={wear} | rarity={rarity} | float={fl}")
    return "\n".join(lines)
