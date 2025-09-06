import time
import requests
from typing import Any, Dict, List

from models.listing_models import ItemDTO
from config.settings import LISTINGS_ENDPOINT, ITEM_NAMES_ENDPOINT

DEFAULT_TIMEOUT = (3.05, 10)


# Lightweight client-side error types with user-friendly messages
class ApiClientError(Exception):
    def __init__(self, user_message: str, *, status_code: int | None = None, detail: str | None = None):
        super().__init__(detail or user_message)
        self.user_message = user_message
        self.status_code = status_code
        self.detail = detail


def _map_http_error(status: int, payload: Dict[str, Any] | None) -> ApiClientError:
    server_msg = None
    if isinstance(payload, dict):
        # Backend returns {"error": ..., "message": ...}
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
    return ApiClientError(user_message, status_code=status, detail=str(server_msg) if server_msg else None)


def _request_json(method: str, url: str, *, params: Dict[str, Any] | None = None, json: Any | None = None) -> Dict[str, Any]:
    try:
        resp = requests.request(method, url, params=params, json=json, timeout=DEFAULT_TIMEOUT)
        # Attempt to parse JSON payload early for richer errors
        payload: Dict[str, Any] | None = None
        try:
            payload = resp.json()
        except Exception:
            payload = None

        if not resp.ok:
            raise _map_http_error(resp.status_code, payload)

        if not isinstance(payload, dict):
            raise ApiClientError("Unexpected response format from server.")
        return payload
    except requests.Timeout:
        raise ApiClientError("Request timed out. Please try again.")
    except requests.ConnectionError:
        raise ApiClientError(
            "Cannot reach backend. Verify the server is running and reachable."
        )
    except requests.RequestException as e:
        raise ApiClientError("Network error occurred. Please try again.", detail=str(e))


def _merge_item(entry: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    if "item" in entry and isinstance(entry["item"], dict):
        merged.update(entry["item"])
    merged.update({k: v for k, v in entry.items() if k != "item"})
    return merged


def fetch_listings(params: Dict[str, Any]) -> List[ItemDTO]:
    start = time.time()
    data = _request_json("GET", LISTINGS_ENDPOINT, params=params)

    items_raw = data.get("data")
    if not isinstance(items_raw, list):
        raise ApiClientError("Unexpected listings payload from server.")

    listings = [ItemDTO.from_dict(_merge_item(e)) for e in items_raw if isinstance(e, dict)]

    elapsed = time.time() - start
    if elapsed < 0.1:
        print("[Cache] Using cached listings!")
    else:
        print(f"[Cache] Fetching listings from API... ({elapsed:.2f}s)")
    return listings


def fetch_item_names(limit: int = 50) -> list[str]:
    try:
        data = _request_json("GET", ITEM_NAMES_ENDPOINT, params={"limit": limit})
        names = data.get("names") if isinstance(data, dict) else None
        if not isinstance(names, list):
            return []
        return [str(n) for n in names if isinstance(n, str) and n.strip()]
    except ApiClientError:
        # Silently degrade in the UI (filters can work without names)
        return []
