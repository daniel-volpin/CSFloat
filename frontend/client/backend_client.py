import time
from typing import Any, Dict, List, Optional, Type

import httpx
from config.settings import API_BASE_URL, LISTINGS_ENDPOINT
from models.listing_models import ItemDTO

_client = httpx.Client(
    timeout=httpx.Timeout(connect=3.05, read=10.0, write=10.0, pool=3.0),
)


class ApiClientError(Exception):
    """
    Exception for API client errors.
    Args:
        user_message: User-friendly error message.
        status_code: Optional HTTP status code.
        detail: Optional technical detail.
    """

    def __init__(
        self,
        user_message: str,
        *,
        status_code: int | None = None,
        detail: str | None = None,
    ):
        super().__init__(detail or user_message)
        self.user_message = user_message
        self.status_code = status_code
        self.detail = detail


class BackendApiError(ApiClientError):
    """Exception for backend API errors."""

    pass


def _map_http_error(status: int, payload: Dict[str, Any] | None) -> ApiClientError:
    """
    Map HTTP status and payload to a user-friendly ApiClientError.
    """
    server_msg = None
    if isinstance(payload, dict):
        server_msg = payload.get("message") or payload.get("detail")

    messages = {
        400: "Invalid request. Please adjust filters and try again.",
        401: "Unauthorized. Check your credentials or API key.",
        403: "Forbidden. You do not have access to this resource.",
        404: "Endpoint not found. Ensure the backend is up-to-date.",
        405: "Method not allowed.",
        409: "Conflict. Please retry.",
        422: "Invalid parameters. Please review your inputs.",
        429: "Too many requests. Please wait a moment and retry.",
        500: "Server error. Please try again later.",
        502: "Bad gateway. Please try again later.",
        503: "Service unavailable. Please try again later.",
        504: "Gateway timeout. Please try again later.",
    }
    base = messages.get(status, f"HTTP {status} error.")
    user_message = server_msg if isinstance(server_msg, str) and server_msg.strip() else base
    return ApiClientError(
        user_message, status_code=status, detail=str(server_msg) if server_msg else None
    )


def _request_json(
    method: str,
    url: str,
    *,
    params: Dict[str, Any] | None = None,
    json: Any | None = None,
    error_cls: Type[ApiClientError] = ApiClientError,
) -> Dict[str, Any]:
    """
    Make an HTTP request and return JSON response, raising error_cls on failure.
    """
    try:
        resp = _client.request(method, url, params=params, json=json)
        payload: Dict[str, Any] | None = None
        try:
            payload = resp.json()
        except Exception:
            payload = None

        if not (200 <= resp.status_code < 300):
            raise error_cls(
                (_map_http_error(resp.status_code, payload).user_message),
                status_code=resp.status_code,
                detail=str(payload),
            )

        if not isinstance(payload, dict):
            raise error_cls("Unexpected response format from server.")
        return payload
    except httpx.ConnectTimeout:
        raise error_cls("Connection timed out. Please try again.")
    except httpx.ReadTimeout:
        raise error_cls("Request timed out. Please try again.")
    except httpx.ConnectError:
        raise error_cls("Cannot reach backend. Verify the server is running and reachable.")
    except httpx.HTTPError as e:
        raise error_cls("Network error occurred. Please try again.", detail=str(e))


def _merge_item(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge item dict from API response into a flat dict.
    """
    merged: Dict[str, Any] = {}
    if "item" in entry and isinstance(entry["item"], dict):
        merged.update(entry["item"])
    merged.update({k: v for k, v in entry.items() if k != "item"})
    return merged


def fetch_listings(params: Dict[str, Any]) -> List[ItemDTO]:
    """
    Fetch listings from backend and return as ItemDTO list.
    """
    start = time.time()
    data = _request_json("GET", LISTINGS_ENDPOINT, params=params, error_cls=ApiClientError)

    items_raw = data.get("data")
    if not isinstance(items_raw, list):
        raise ApiClientError("Unexpected listings payload from server.")

    listings = [ItemDTO.from_dict(_merge_item(e)) for e in items_raw if isinstance(e, dict)]

    elapsed = time.time() - start
    meta = data.get("meta")
    if isinstance(meta, dict) and meta.get("cache") == "HIT":
        print("[Cache] Using cached listings!")
    else:
        print(f"[Cache] Fetching listings from API... ({elapsed:.2f}s)")
    return listings


class BackendClient:
    """
    Client for backend analysis and listings.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or API_BASE_URL

    def fetch_listings(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch listings from backend API.
        """
        data = _request_json(
            "GET", f"{self.base_url}/api/listings", params=params, error_cls=BackendApiError
        )
        results = data.get("data")
        return results if isinstance(results, list) else []

    def list_llm_models(self) -> List[Dict[str, Any]]:
        """
        List available LLM models from backend.
        """
        data = _request_json("GET", f"{self.base_url}/llm/models", error_cls=BackendApiError)
        models = data.get("models")
        return models if isinstance(models, list) else []

    def analyze_listings(
        self,
        question: str,
        items: List[Any],
        model: Optional[str] = None,
        max_items: int = 50,
    ) -> str:
        """
        Analyze listings with AI via backend.
        """
        serializable_items = [item.dict() if hasattr(item, "dict") else item for item in items]
        payload = {
            "question": question,
            "items": serializable_items,
            "model": model,
            "max_items": max_items,
        }
        data = _request_json(
            "POST", f"{self.base_url}/api/analyze", json=payload, error_cls=BackendApiError
        )
        return data.get("result") or data.get("answer") or "No answer returned."
