import pytest
from fastapi.testclient import TestClient

import backend.features.listings.router as listings_router
from backend.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestListingsAPI:
    @pytest.fixture(autouse=True)
    def setup_method(self, monkeypatch):
        self.monkeypatch = monkeypatch

    @pytest.mark.parametrize(
        "mock_items,expected_names",
        [
            (
                [
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
                ],
                {"AK-47 | Redline", "M4A1-S | Golden Coil"},
            ),
            (
                [
                    {
                        "name": "AK-47 | Redline",
                        "price": 12345,
                        "wear": "Field-Tested",
                        "rarity": "Rare",
                        "float_value": 0.123456,
                    }
                ],
                {"AK-47 | Redline"},
            ),
        ],
    )
    def test_given_valid_params_when_get_listings_then_return_expected_items(
        self, client, mock_items, expected_names
    ):
        # Arrange
        def fake_fetch_listings(params):
            return mock_items, "MISS"

        self.monkeypatch.setattr(
            listings_router.csfloat_client, "fetch_listings", fake_fetch_listings
        )

        # Act
        resp = client.get("/listings", params={"limit": len(mock_items)})

        # Assert
        assert resp.status_code == 200
        data = resp.json()
        assert "data" in data and isinstance(data["data"], list)
        names = {item["name"] for item in data["data"]}
        assert expected_names.issubset(names)
        assert "meta" in data and "cache" in data["meta"]

    def test_given_upstream_down_when_get_listings_then_return_503(self, client):
        # Arrange
        def boom(_):
            raise RuntimeError("upstream down")

        self.monkeypatch.setattr(listings_router.csfloat_client, "fetch_listings", boom)

        # Act
        resp = client.get("/listings")

        # Assert
        assert resp.status_code == 503
        msg = resp.json().get("message", "").lower()
        assert "unavailable" in msg
