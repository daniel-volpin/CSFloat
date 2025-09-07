from __future__ import annotations

from typing import Any, Dict, Optional


def _is_number_str(s: str) -> bool:
    try:
        float(s)
        return True
    except Exception:
        return False


def normalize_listings_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize incoming query params for CSFloat upstream API.

    - Drop None/empty values
    - Convert dollar prices (float) -> cents (int) for min_price/max_price
    - Ensure range constraints (min <= max) for float and price
    - Keep list-like params as-is if non-empty
    """
    normalized: Dict[str, Any] = {}

    # Start with a shallow copy to avoid mutating input
    raw = dict(params or {})

    # Basic passthrough keys
    passthrough_keys = [
        "cursor",
        "limit",
        "sort_by",
        "category",
        "def_index",
        "rarity",
        "paint_seed",
        "paint_index",
        "user_id",
        "collection",
        "market_hash_name",
        "item_name",
        "type",
        "stickers",
    ]

    # Floats range
    min_float = raw.get("min_float")
    max_float = raw.get("max_float")
    try:
        mf = float(min_float) if min_float is not None else None
        xf = float(max_float) if max_float is not None else None
    except Exception:
        mf = None
        xf = None
    if mf is not None and xf is not None:
        if mf > xf:
            mf, xf = xf, mf
        mf = max(0.0, min(1.0, mf))
        xf = max(0.0, min(1.0, xf))
    if mf is not None:
        normalized["min_float"] = mf
    if xf is not None:
        normalized["max_float"] = xf

    # Price range: dollars -> cents
    min_price = raw.get("min_price")
    max_price = raw.get("max_price")

    def _to_cents(v: Any) -> Optional[int]:
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return int(float(v) * 100)
        if isinstance(v, str) and _is_number_str(v):
            return int(float(v) * 100)
        return None

    mp = _to_cents(min_price)
    xp = _to_cents(max_price)
    if mp is not None and xp is not None and mp > xp:
        mp, xp = xp, mp
    if mp is not None and mp >= 0:
        normalized["min_price"] = mp
    if xp is not None and xp >= 0:
        normalized["max_price"] = xp

    # Passthrough (filter out empties)
    for key in passthrough_keys:
        val = raw.get(key)
        if val is None:
            continue
        if isinstance(val, str) and not val.strip():
            continue
        if isinstance(val, (list, dict)) and not val:
            continue
        normalized[key] = val

    return normalized
