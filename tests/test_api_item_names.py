from fastapi.testclient import TestClient

from backend.main import app


def test_item_names_success(monkeypatch):
    from backend.api import item_names as item_names_mod

    def fake_fetch(limit: int = 50):
        return ["AK-47 | Redline", "M4A1-S | Golden Coil"][:limit]

    monkeypatch.setattr(item_names_mod, "fetch_csfloat_item_names", fake_fetch)
    client = TestClient(app)
    resp = client.get("/api/item-names", params={"limit": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert data["names"] == ["AK-47 | Redline", "M4A1-S | Golden Coil"]


def test_item_names_failure(monkeypatch):
    from backend.api import item_names as item_names_mod

    def boom(limit: int = 50):  # noqa: ARG001
        raise RuntimeError("oops")

    monkeypatch.setattr(item_names_mod, "fetch_csfloat_item_names", boom)
    client = TestClient(app)
    resp = client.get("/api/item-names")
    assert resp.status_code == 503
    assert "unavailable" in resp.json().get("message", "").lower()
