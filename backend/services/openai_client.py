import os
from typing import Optional

import httpx
from openai import OpenAI

from ..config.settings import get_settings


class OpenAIClient:
    """
    Wrapper for OpenAI client creation and chat completion calls.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        settings = get_settings()
        self.api_key = api_key or settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or settings.OPENAI_BASE_URL or os.getenv("OPENAI_BASE_URL")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        http_client = self._build_http_client()
        if self.base_url:
            self.client = OpenAI(
                api_key=self.api_key, base_url=self.base_url, http_client=http_client
            )
        else:
            self.client = OpenAI(api_key=self.api_key, http_client=http_client)

    def _build_http_client(self) -> httpx.Client | None:
        """Build an httpx client that respects environment proxy settings.

        We avoid passing unsupported kwargs into the OpenAI SDK by constructing
        our own httpx client and handing it in via `http_client`. Rely on
        `trust_env=True` so standard env vars (HTTP(S)_PROXY, ALL_PROXY) are used.
        """
        timeout = httpx.Timeout(connect=10.0, read=30.0, write=30.0, pool=5.0)
        try:
            return httpx.Client(timeout=timeout, trust_env=True)
        except Exception:
            return None

    def chat(
        self,
        model: str,
        messages: list,
        temperature: float = 0.2,
        max_tokens: int = 300,
    ) -> str:
        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or "(No response)"
