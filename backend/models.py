from pydantic import BaseModel
from typing import Optional, List


class ItemDTO(BaseModel):
    name: Optional[str]
    price: Optional[int]
    wear: Optional[str]
    rarity: Optional[str]
    float_value: Optional[float]


def item_to_dto(item):
    """
    Converts an item dict or object to ItemDTO, extracting only relevant fields.
    """
    if isinstance(item, dict):
        return ItemDTO(
            name=item.get("name"),
            price=item.get("price"),
            wear=item.get("wear"),
            rarity=item.get("rarity"),
            float_value=item.get("float_value"),
        )
    else:
        return ItemDTO(
            name=getattr(item, "name", None),
            price=getattr(item, "price", None),
            wear=getattr(item, "wear", None),
            rarity=getattr(item, "rarity", None),
            float_value=getattr(item, "float_value", None),
        )


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
    item_name: Optional[str] = None
    type: Optional[str] = None
    stickers: Optional[str] = None
