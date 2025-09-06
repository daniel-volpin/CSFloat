# models.py - Data models for frontend

class ItemDTO:
    def __init__(self, name, price, wear, rarity, float_value):
        self.name = name
        self.price = price
        self.wear = wear
        self.rarity = rarity
        self.float_value = float_value

    @classmethod
    def from_dict(cls, data):
        # Map fields from merged dict
        name = data.get('item_name') or data.get('name')
        price = data.get('price')
        wear = data.get('wear_name') or data.get('wear')
        # Rarity: prefer string, fallback to int
        rarity = data.get('rarity')
        if isinstance(rarity, int):
            rarity_map = {
                1: "Common", 2: "Uncommon", 3: "Rare", 4: "Mythical", 5: "Legendary", 6: "Ancient", 7: "Immortal"
            }
            rarity = rarity_map.get(rarity, str(rarity))
        float_value = data.get('float_value')
        return cls(name, price, wear, rarity, float_value)
