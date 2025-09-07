import pytest

from backend.services.csfloat.params import normalize_listings_params


class TestNormalizeListingsParams:
    @pytest.mark.parametrize(
        "params",
        [
            {"min_price": 200.0, "max_price": 100.0},
            {"min_price": "12.34", "max_price": "56.78"},
        ],
    )
    def test_given_price_params_when_normalize_then_prices_are_dropped(self, params):
        # Arrange

        # Act
        out = normalize_listings_params(params)

        # Assert
        assert "min_price" not in out
        assert "max_price" not in out

    @pytest.mark.parametrize(
        "params,expected_min,expected_max",
        [
            ({"min_float": 1.2, "max_float": -0.5}, -0.5, 1.2),
            ({"min_float": -0.1, "max_float": 0.9}, -0.1, 0.9),
        ],
    )
    def test_given_float_range_when_normalize_then_swaps_if_needed(
        self, params, expected_min, expected_max
    ):
        # Arrange

        # Act
        out = normalize_listings_params(params)

        # Assert
        assert out["min_float"] == expected_min
        assert out["max_float"] == expected_max

    def test_given_empty_and_list_params_when_normalize_then_drops_non_float_keys(self):
        # Arrange
        params = {
            "cursor": "",
            "stickers": "  ",
            "def_index": [1, 2, 3],
            "paint_seed": [],
            "min_price": None,
            "max_price": None,
        }

        # Act
        out = normalize_listings_params(params)

        # Assert
        assert out == {}
