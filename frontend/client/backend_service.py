import os
import requests
from typing import Any, Dict, List, Optional

DEFAULT_TIMEOUT = (3.05, 15)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


class BackendApiError(Exception):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


def _request_json(method: str, url: str, *, params: Dict[str, Any] | None = None, json: Any | None = None) -> Dict[str, Any]:
    try:
        resp = requests.request(method, url, params=params, json=json, timeout=DEFAULT_TIMEOUT)
        try:
            payload = resp.json()
        except Exception:
            payload = None
        if not resp.ok:
            message = None
            if isinstance(payload, dict):
                message = payload.get("message") or payload.get("detail")
            raise BackendApiError(message or f"HTTP {resp.status_code} error", status=resp.status_code)
        if not isinstance(payload, dict):
            raise BackendApiError("Unexpected response format from backend")
        return payload
    except requests.Timeout:
        raise BackendApiError("Request to backend timed out")
    except requests.ConnectionError:
        raise BackendApiError("Cannot reach backend service")
    except requests.RequestException as e:
        raise BackendApiError(f"Network error: {e}")


class BackendClient:
    """
    Client for communicating with the backend API.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or BACKEND_URL

    def fetch_listings(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = _request_json("GET", f"{self.base_url}/api/listings", params=params)
        results = data.get("data")
        return results if isinstance(results, list) else []

    def analyze_listings(
        self,
        question: str,
        items: List[Any],
        model: Optional[str] = None,
        max_items: int = 50,
    ) -> str:
        serializable_items = [item.dict() if hasattr(item, "dict") else item for item in items]
        payload = {"question": question, "items": serializable_items, "model": model, "max_items": max_items}
        data = _request_json("POST", f"{self.base_url}/api/analyze", json=payload)
        # Backend currently returns {"result": ...}
        return (
            data.get("result")
            or data.get("answer")
            or "No answer returned."
        )
