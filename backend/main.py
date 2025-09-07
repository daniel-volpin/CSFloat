from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api import router
from .config.settings import get_settings
from .services.csfloat.client import CSFloatClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    http2_enabled = bool(settings.HTTP2_ENABLED)
    try:
        if http2_enabled:
            pass
        else:
            http2_enabled = False
    except Exception:
        http2_enabled = False

    client = httpx.Client(
        http2=http2_enabled,
        timeout=httpx.Timeout(
            connect=float(settings.REQUEST_CONNECT_TIMEOUT),
            read=float(settings.REQUEST_READ_TIMEOUT),
            write=float(settings.REQUEST_READ_TIMEOUT),
            pool=float(settings.HTTPX_POOL_TIMEOUT),
        ),
        limits=httpx.Limits(
            max_keepalive_connections=int(settings.HTTPX_MAX_KEEPALIVE),
            max_connections=int(settings.HTTPX_MAX_CONNECTIONS),
        ),
    )
    csfloat_client = CSFloatClient()
    csfloat_client.set_http_client(client)
    try:
        yield
    finally:
        client.close()


app = FastAPI(lifespan=lifespan)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(_settings.CORS_ALLOW_ORIGINS or ["*"]),
    allow_credentials=bool(_settings.CORS_ALLOW_CREDENTIALS),
    allow_methods=list(_settings.CORS_ALLOW_METHODS or ["*"]),
    allow_headers=list(_settings.CORS_ALLOW_HEADERS or ["*"]),
)

app.include_router(router, prefix="/api")


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Invalid request parameters.",
            "details": exc.errors(),
        },
    )
