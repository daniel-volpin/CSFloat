from typing import Any

from .service import ask_about_listings


class LLMClient:
    def ask_about_listings(self, *args: Any, **kwargs: Any) -> str:
        return ask_about_listings(*args, **kwargs)
