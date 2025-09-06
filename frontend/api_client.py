# api_client.py - API interaction logic for frontend
import requests
from models import ItemDTO

def fetch_listings(params):
    response = requests.get("http://localhost:8000/api/listings", params=params)
    response.raise_for_status()
    data = response.json()
    listings = []
    for entry in data:
        merged = {}
        if 'item' in entry and isinstance(entry['item'], dict):
            merged.update(entry['item'])
        merged.update({k: v for k, v in entry.items() if k != 'item'})
        listings.append(ItemDTO.from_dict(merged))
    return listings
