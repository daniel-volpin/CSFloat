from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class FilterState(BaseModel):
    """Represents the sidebar filter UI state and maps to API params.

    Store raw UI selections and provide a `to_params()` transformer
    so the rendering code stays clean and the mapping logic is centralized.
    """

    # Basic
    cursor: Optional[str] = Field(None, description="API cursor for pagination")
    limit: int = Field(10, description="Maximum number of items to fetch")
    sort_by: str = Field("best_deal", description="Sort order for listings")
    category: str = Field("Any", description="Item category filter")
    def_index: Optional[List[int]] = Field(None, description="Definition indices for items")

    # Float & Rarity
    min_float: float = Field(0.0, description="Minimum float value for item filter")
    max_float: float = Field(1.0, description="Maximum float value for item filter")
    rarity_selections: List[str] = Field(
        default_factory=list, description="Selected rarities for filter"
    )

    # Item details
    paint_seed: Optional[List[int]] = Field(None, description="Paint seed values for item filter")
    paint_index: Optional[int] = Field(None, description="Paint index for item filter")
    user_id: Optional[str] = Field(None, description="User ID for filtering items")
    collection: Optional[str] = Field(None, description="Collection name for filtering items")

    # Misc
    market_hash_name: Optional[str] = Field(None, description="Market hash name for manual search")
    type: Optional[str] = Field(None, description="Type of listing (buy_now, auction, etc.)")
    stickers: Optional[str] = Field(None, description="Sticker information for item filter")

    # Price (USD)
    min_price: Optional[float] = Field(None, description="Minimum price in USD")
    max_price: Optional[float] = Field(None, description="Maximum price in USD")

    def to_params(
        self, *, category_map: Dict[str, int], rarity_map: Dict[str, int | None]
    ) -> Dict[str, object]:
        """Convert UI state to backend API param dict."""
        rarity_val = None
        if self.rarity_selections and len(self.rarity_selections) == 1:
            rarity_val = rarity_map.get(self.rarity_selections[0])

        params: Dict[str, object] = {
            "cursor": self.cursor or None,
            "limit": int(self.limit),
            "sort_by": self.sort_by,
            "category": category_map.get(self.category, 0),
            "def_index": self.def_index or None,
            "min_float": float(self.min_float),
            "max_float": float(self.max_float),
            "rarity": rarity_val,
            "paint_seed": self.paint_seed or None,
            "paint_index": int(self.paint_index) if self.paint_index is not None else None,
            "user_id": self.user_id or None,
            "collection": self.collection or None,
            "market_hash_name": self.market_hash_name or None,
            "type": self.type or None,
            "stickers": self.stickers or None,
            # Send prices in dollars; backend converts to cents for upstream API
            "min_price": float(self.min_price) if self.min_price else None,
            "max_price": float(self.max_price) if self.max_price else None,
        }
        return params
