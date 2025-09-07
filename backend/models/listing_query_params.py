from typing import List, Optional

from pydantic import BaseModel


class ListingQueryParams(BaseModel):
    cursor: Optional[str] = None
    limit: Optional[int] = 50
    sort_by: Optional[str] = "best_deal"
    category: Optional[int] = 0
    def_index: Optional[List[int]] = None
    min_float: Optional[float] = None
    max_float: Optional[float] = None
    rarity: Optional[int] = None
    paint_seed: Optional[List[int]] = None
    paint_index: Optional[int] = None
    user_id: Optional[str] = None
    collection: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    market_hash_name: Optional[str] = None
    item_name: Optional[str] = None
    type: Optional[str] = None
    stickers: Optional[str] = None
