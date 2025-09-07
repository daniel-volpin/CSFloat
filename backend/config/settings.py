from __future__ import annotations

from functools import lru_cache
from typing import List, Tuple

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # CSFloat API
    CSFLOAT_API_KEY: str | None = None
    CSFLOAT_API_URL: str = "https://csfloat.com/api/v1/listings"
    CSFLOAT_ITEM_NAMES_URL: str = "https://csfloat.com/api/v1/item-names"

    # HTTP client
    REQUEST_CONNECT_TIMEOUT: float = 3.05
    REQUEST_READ_TIMEOUT: float = 10.0

    # Cache
    CACHE_TTL_SECONDS: int = 600
    CACHE_MAXSIZE: int = 128
    SINGLE_FLIGHT_WAIT_SECONDS: float = 3.0

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # LLM provider selection
    # Values: "openai" (default), "lmstudio"
    LLM_PROVIDER: str = "openai"
    # Optional LM Studio overrides
    LMSTUDIO_API_HOST: str | None = None
    LMSTUDIO_MODEL: str | None = None

    # HTTPX client tuning
    HTTP2_ENABLED: bool = True
    HTTPX_MAX_KEEPALIVE: int = 20
    HTTPX_MAX_CONNECTIONS: int = 50
    HTTPX_POOL_TIMEOUT: float = 3.0

    # CORS
    CORS_ALLOW_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    model_config = SettingsConfigDict(env_file=("backend/.env", ".env"), extra="ignore")

    @property
    def requests_timeout(self) -> Tuple[float, float]:
        return (float(self.REQUEST_CONNECT_TIMEOUT), float(self.REQUEST_READ_TIMEOUT))

    @field_validator("CORS_ALLOW_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:  # type: ignore[override]
        """Allow comma-separated string or JSON list for CORS origins.

        Examples:
        - CORS_ALLOW_ORIGINS=["http://localhost:8501","http://localhost:3000"]
        - CORS_ALLOW_ORIGINS=http://localhost:8501,http://localhost:3000
        """
        if isinstance(v, str):
            raw = [s.strip() for s in v.split(",")]
            vals = [s for s in raw if s]
            return vals or ["*"]
        return v


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
