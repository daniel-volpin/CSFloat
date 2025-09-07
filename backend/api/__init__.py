from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"message": "pong"}


try:
    from .analyze import router as analyze_router

    router.include_router(analyze_router)

    from .listings import router as listings_router

    router.include_router(listings_router)

    from .item_names import router as item_names_router

    router.include_router(item_names_router)

    from .cache import router as cache_router

    router.include_router(cache_router)

    from .models import router as models_router

    router.include_router(models_router)
except Exception:  # pragma: no cover
    pass
