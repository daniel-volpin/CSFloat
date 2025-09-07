from fastapi.testclient import TestClient

from backend.api import listings as listings_mod
from backend.main import app


def test_listings_endpoint_success(monkeypatch):

    def fake_fetch(params):
        # Return two simple items and a cache status
        items = [
            {
                "name": "AK-47 | Redline",
                "price": 12345,
                "wear": "Field-Tested",
                "rarity": "Rare",
                "float_value": 0.123456,
            },
            {
                "name": "M4A1-S | Golden Coil",
                "price": 67890,
                "wear": "Minimal Wear",
                "rarity": "Legendary",
                "float_value": 0.045678,
            },
        ]
        return items, "MISS"

    monkeypatch.setattr(listings_mod, "fetch_csfloat_listings", fake_fetch)

    client = TestClient(app)
    resp = client.get("/api/listings", params={"limit": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert "data" in data and isinstance(data["data"], list)
    assert len(data["data"]) == 2
    assert data.get("meta", {}).get("cache") == "MISS"


def test_listings_endpoint_failure(monkeypatch):
    from backend.api import listings as listings_mod

    def boom(_):
        raise RuntimeError("upstream down")

    monkeypatch.setattr(listings_mod, "fetch_csfloat_listings", boom)
    client = TestClient(app)
    resp = client.get("/api/listings")
    assert resp.status_code == 503
    assert "unavailable" in resp.json().get("message", "").lower()
