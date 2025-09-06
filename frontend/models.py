from pydantic import BaseModel
from typing import Optional, Any


class ItemDTO(BaseModel):
    name: Optional[str]
    price: Optional[int]
    wear: Optional[str]
    rarity: Optional[str]
    float_value: Optional[float]

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
        return cls(
            name=name, price=price, wear=wear, rarity=rarity, float_value=float_value
        )
