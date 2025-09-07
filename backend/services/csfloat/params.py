from typing import Any, Dict


def normalize_listings_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize incoming query params for CSFloat upstream API.
    - Drop None/empty values
    - Convert dollar prices (float) -> cents (int) for min_price/max_price
    - Ensure range constraints (min <= max) for float and price
    - Keep list-like params as-is if non-empty
    """
    normalized: Dict[str, Any] = {}
    raw = dict(params or {})

    def normalize_range(a, b):
        try:
            va = float(a) if a is not None else None
            vb = float(b) if b is not None else None
            if va is not None and vb is not None and va > vb:
                va, vb = vb, va
            return va, vb
        except Exception:
            return a, b

    min_float = raw.get("min_float")
    max_float = raw.get("max_float")
    min_price = raw.get("min_price")
    max_price = raw.get("max_price")

    mf, xf = normalize_range(min_float, max_float)
    mp, xp = normalize_range(min_price, max_price)

    if mf is not None:
        normalized["min_float"] = mf
    if xf is not None:
        normalized["max_float"] = xf
    if mp is not None:
        normalized["min_price"] = int(mp)
    if xp is not None:
        normalized["max_price"] = int(xp)

    # ...existing logic from csfloat_params.py continues...
    return normalized
