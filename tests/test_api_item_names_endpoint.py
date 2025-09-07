import pytest
from fastapi.testclient import TestClient

import backend.features.item_names.router as item_names_router
from backend.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestItemNamesAPI:
    @pytest.fixture(autouse=True)
    def setup_method(self, monkeypatch):
        self.monkeypatch = monkeypatch

    @pytest.mark.parametrize(
        "limit,expected_names",
        [
            (2, {"AK-47 | Redline", "M4A1-S | Golden Coil"}),
            (1, {"AK-47 | Redline"}),
        ],
    )
    def test_given_valid_limit_when_get_item_names_then_return_expected_names(
        self, client, limit, expected_names
    ):
        # Arrange
        def fake_fetch_item_names(limit: int = 50):
            return ["AK-47 | Redline", "M4A1-S | Golden Coil"][:limit]

        self.monkeypatch.setattr(
            item_names_router.csfloat_client, "fetch_item_names", fake_fetch_item_names
        )

        # Act
        resp = client.get("/item-names", params={"limit": limit})

        # Assert
        assert resp.status_code == 200
        data = resp.json()
        assert set(data["names"]) == expected_names

    def test_given_upstream_down_when_get_item_names_then_return_503(self, client):
        # Arrange
        def boom(limit: int = 50):
            raise RuntimeError("oops")

        self.monkeypatch.setattr(item_names_router.csfloat_client, "fetch_item_names", boom)

        # Act
        resp = client.get("/item-names")

        # Assert
        assert resp.status_code == 503
        msg = resp.json().get("message", resp.json().get("detail", "")).lower()
        assert "unavailable" in msg
