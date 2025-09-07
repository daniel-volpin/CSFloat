from __future__ import annotations

from functools import lru_cache
from typing import Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # CSFloat API
    CSFLOAT_API_KEY: str | None = None
    CSFLOAT_API_URL: str = "https://csfloat.com/api/v1/listings"
    CSFLOAT_ITEM_NAMES_URL: str = "https://api.csfloat.com/api/v1/item-names"

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

    # HTTPX client tuning
    HTTP2_ENABLED: bool = True
    HTTPX_MAX_KEEPALIVE: int = 20
    HTTPX_MAX_CONNECTIONS: int = 50
    HTTPX_POOL_TIMEOUT: float = 3.0

    model_config = SettingsConfigDict(env_file=("backend/.env", ".env"), extra="ignore")

    @property
    def requests_timeout(self) -> Tuple[float, float]:
        return (float(self.REQUEST_CONNECT_TIMEOUT), float(self.REQUEST_READ_TIMEOUT))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
