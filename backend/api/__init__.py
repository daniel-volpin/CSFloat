from fastapi import APIRouter

router = APIRouter()


# Example route (health)
@router.get("/ping")
async def ping():
    return {"message": "pong"}


# Include feature routers here to expose endpoints under /api
try:
    from .analyze import router as analyze_router

    router.include_router(analyze_router)

    from .listings import router as listings_router

    router.include_router(listings_router)

    from .cache import router as cache_router

    router.include_router(cache_router)
except Exception:  # pragma: no cover - avoid import errors at startup
    # If subrouter import fails (e.g., during incomplete refactors), keep API up.
    pass
