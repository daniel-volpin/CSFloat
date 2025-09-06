import requests
import os
from typing import Any, Dict, List, Optional

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


class BackendClient:
    """
    Client for communicating with the backend API.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or BACKEND_URL

    def fetch_listings(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        resp = requests.get(f"{self.base_url}/listings", params=params)
        resp.raise_for_status()
        return resp.json()

    def analyze_listings(
        self,
        question: str,
        items: List[Any],
        model: Optional[str] = None,
        max_items: int = 50,
    ) -> str:
        # Ensure all items are dicts for JSON serialization
        serializable_items = [
            item.dict() if hasattr(item, "dict") else item for item in items
        ]
        payload = {
            "question": question,
            "items": serializable_items,
            "model": model,
            "max_items": max_items,
        }
        resp = requests.post(f"{self.base_url}/api/analyze", json=payload)
        resp.raise_for_status()
        return resp.json().get("answer", "No answer returned.")
