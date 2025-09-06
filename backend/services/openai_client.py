import os
from typing import Optional

from openai import OpenAI

from ..core.utils import OPENAI_API_KEY


class OpenAIClient:
    """
    Wrapper for OpenAI client creation and chat completion calls.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        if self.base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = OpenAI(api_key=self.api_key)

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
