from pydantic import BaseModel
from typing import Optional, List

class ListingQueryParams(BaseModel):
    cursor: Optional[str] = None
    limit: Optional[int] = 50
    sort_by: Optional[str] = "best_deal"
    category: Optional[int] = 0
    def_index: Optional[List[int]] = None
    min_float: Optional[float] = None
    max_float: Optional[float] = None
    rarity: Optional[str] = None
    paint_seed: Optional[int] = None
    paint_index: Optional[int] = None
    user_id: Optional[str] = None
    collection: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    market_hash_name: Optional[str] = None
    type: Optional[str] = None
    stickers: Optional[str] = None
