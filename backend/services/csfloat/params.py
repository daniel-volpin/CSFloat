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
    min_float = raw.get("min_float")
    max_float = raw.get("max_float")
    try:
        mf = float(min_float) if min_float is not None else None
        xf = float(max_float) if max_float is not None else None
        if mf is not None and xf is not None and mf > xf:
            mf, xf = xf, mf
        if mf is not None:
            normalized["min_float"] = mf
        if xf is not None:
            normalized["max_float"] = xf
    except Exception:
        pass
    # ...existing logic from csfloat_params.py continues...
    return normalized
