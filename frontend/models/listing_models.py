from typing import Any, Optional

from pydantic import BaseModel, Field


class ItemDTO(BaseModel):
    name: Optional[str] = Field(None, description="Name of the item")
    price: Optional[int] = Field(None, description="Price of the item in cents")
    wear: Optional[str] = Field(None, description="Wear level or condition of the item")
    rarity: Optional[str] = Field(None, description="Rarity classification of the item")
    float_value: Optional[float] = Field(None, description="Float value indicating item quality")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ItemDTO":
        name = data.get("item_name") or data.get("name")
        price = data.get("price")
        wear = data.get("wear_name") or data.get("wear")
        rarity = data.get("rarity")
        if isinstance(rarity, int):
            rarity_map = {
                1: "Common",
                2: "Uncommon",
                3: "Rare",
                4: "Mythical",
                5: "Legendary",
                6: "Ancient",
                7: "Immortal",
            }
            rarity = rarity_map.get(rarity, str(rarity))
        float_value = data.get("float_value")
        return cls(name=name, price=price, wear=wear, rarity=rarity, float_value=float_value)
