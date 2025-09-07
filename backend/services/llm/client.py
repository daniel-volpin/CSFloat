from .service import ask_about_listings


class LLMClient:
    def ask_about_listings(self, *args, **kwargs):
        return ask_about_listings(*args, **kwargs)
