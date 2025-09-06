import os
from typing import List, Optional
from openai import OpenAI
from models import ItemDTO


def _build_listings_digest(items: List[ItemDTO], max_items: int = 50) -> str:
    lines = []
    for i, it in enumerate(items[: max_items if max_items > 0 else 50], start=1):
        price_str = f"${(it.price or 0) / 100:.2f}" if it.price is not None else "N/A"
        wear = it.wear or "N/A"
        rarity = it.rarity or "N/A"
        fl = f"{it.float_value:.6f}" if it.float_value is not None else "N/A"
        name = it.name or "Unknown"
        lines.append(
            f"{i}. {name} | {price_str} | wear={wear} | rarity={rarity} | float={fl}"
        )
    return "\n".join(lines)


def _make_client() -> OpenAI:
    """Create an OpenAI client (OpenAI only).

    Supported env vars:
    - OPENAI_API_KEY (required)
    - OPENAI_BASE_URL (optional)
    - OPENAI_MODEL (optional)
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    openai_base = os.getenv("OPENAI_BASE_URL")

    # Guard against outdated httpx causing 'proxies' TypeError
    try:
        import httpx  # type: ignore

        ver = getattr(httpx, "__version__", "0.0.0")
        parts = ver.split(".")
        major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        if (major, minor) < (0, 27):
            raise RuntimeError(
                f"httpx {ver} is too old; please upgrade to >= 0.27.0 (pip install -U httpx)."
            )
    except ModuleNotFoundError:
        # If httpx isn't present, OpenAI will install a compatible version via deps
        pass
    if not openai_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    if openai_base:
        return OpenAI(api_key=openai_key, base_url=openai_base)
    return OpenAI(api_key=openai_key)


def ask_about_listings(
    question: str,
    items: List[ItemDTO],
    model: Optional[str] = None,
    max_items: int = 50,
) -> str:
    """Query an LLM about the in-memory listings.

    Args:
        question: User question about the current listings.
        items: List of ItemDTO items currently displayed.
        model: Optional model/deployment name (falls back to env or default).
        max_items: Cap of items to include in the prompt to control token usage.
    Returns:
        AI answer as Markdown string.
    """
    if not items:
        return "No listings are loaded. Adjust filters and try again."

    client = _make_client()

    # Choose model priority: explicit arg → OPENAI_MODEL → sensible default
    chosen_model = model or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"

    digest = _build_listings_digest(items, max_items=max_items)

    system = (
        "You analyze CS:GO marketplace listings for investing. "
        "Be precise and concise. Prefer numeric comparisons (price, float). "
        "If the question is ambiguous, ask for clarification briefly. "
        "Only use the provided listings; do not assume external pricing."
    )

    user = (
        "Here are the current listings (index. name | price | wear | rarity | float):\n\n"
        f"{digest}\n\n"
        f"Question: {question}\n\n"
        "Instructions: If recommending items, reference them by index and name, "
        "explain the rationale (e.g., low float, rarity, price), and suggest 3–5 options at most."
    )

    try:
        resp = client.chat.completions.create(
            model=chosen_model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content or "(No response)"
    except Exception as e:
        msg = str(e)
        if "proxies" in msg and "unexpected keyword" in msg:
            return (
                "LLM request failed due to an old httpx version.\n"
                "Please upgrade httpx to >= 0.27.0 in your frontend environment:\n\n"
                "    pip install -U httpx\n\n"
                f"Details: {e}"
            )
        return (
            "LLM request failed. Ensure OPENAI_API_KEY is set and the model exists.\n\n"
            f"Details: {e}"
        )
