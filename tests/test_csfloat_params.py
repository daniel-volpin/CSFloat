from backend.services.csfloat_params import normalize_listings_params


def test_normalize_prices_swaps_and_converts_to_cents():
    params = {"min_price": 200.0, "max_price": 100.0}
    out = normalize_listings_params(params)
    # Dollars -> cents and swapped
    assert out["min_price"] == 10000
    assert out["max_price"] == 20000


def test_normalize_float_range_clamped_and_swapped():
    params = {"min_float": 1.2, "max_float": -0.5}
    out = normalize_listings_params(params)
    # Swap then clamp to [0.0, 1.0]
    assert out["min_float"] == 0.0
    assert out["max_float"] == 1.0


def test_drop_empty_values_and_passthrough_lists():
    params = {
        "cursor": "",
        "stickers": "  ",
        "def_index": [1, 2, 3],
        "paint_seed": [],
        "min_price": None,
        "max_price": None,
    }
    out = normalize_listings_params(params)
    assert "cursor" not in out
    assert "stickers" not in out
    assert out["def_index"] == [1, 2, 3]
    assert "paint_seed" not in out


def test_accept_string_prices():
    params = {"min_price": "12.34", "max_price": "56.78"}
    out = normalize_listings_params(params)
    assert out["min_price"] == 1234
    assert out["max_price"] == 5678
