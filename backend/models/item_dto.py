from typing import Optional

from pydantic import BaseModel


class ItemDTO(BaseModel):
    name: Optional[str]
    price: Optional[int]
    wear: Optional[str]
    rarity: Optional[str]
    float_value: Optional[float]


def item_to_dto(item):
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
