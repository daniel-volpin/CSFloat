from fastapi import APIRouter

from ..services.csfloat_client import get_cache_stats, invalidate_cache

router = APIRouter()


@router.get("/cache")
def view_cache():
    """View the current listings cache stats."""
    return {"cache": get_cache_stats()}


@router.post("/cache/invalidate")
def clear_cache():
    """Invalidate (clear) the listings cache."""
    invalidate_cache()
    return {"message": "Cache invalidated."}
