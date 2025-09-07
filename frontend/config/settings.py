import os

from dotenv import load_dotenv

# Ensure .env is loaded before reading env vars
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
LISTINGS_ENDPOINT = f"{API_BASE_URL}/api/listings"

# UI settings
APP_TITLE = "CSFloat Listings"
APP_SUBTITLE = "Find and filter your favorite items"

# Filter defaults
DEFAULT_LIMIT = 10
DEFAULT_FLOAT_RANGE = (0.0, 1.0)
# Default index in SORT_OPTIONS for UI ("best_deal")
DEFAULT_SORT_INDEX = 6
RARITY_OPTIONS = [
    "",
    "Common",
    "Uncommon",
    "Rare",
    "Mythical",
    "Legendary",
    "Ancient",
    "Immortal",
]

# Centralized rarity mapping for API use
RARITY_MAP = {
    "": None,
    "Common": 1,
    "Uncommon": 2,
    "Rare": 3,
    "Mythical": 4,
    "Legendary": 5,
    "Ancient": 6,
    "Immortal": 7,
}
CATEGORY_OPTIONS = ["Any", "Normal", "StatTrak", "Souvenir"]
CATEGORY_MAP = {"Any": 0, "Normal": 1, "StatTrak": 2, "Souvenir": 3}
SORT_OPTIONS = [
    "lowest_price",
    "highest_price",
    "most_recent",
    "expires_soon",
    "lowest_float",
    "highest_float",
    "best_deal",
    "highest_discount",
    "float_rank",
    "num_bids",
]
