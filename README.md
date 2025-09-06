# CSFloat — Listings Explorer

## Overview
- Purpose: A two-tier tool for discovering and filtering CS:GO item listings via a lightweight FastAPI backend wrapper around the CSFloat marketplace and a Streamlit UI for investors and collectors.
- What it does: Lets you filter by price, float, rarity, paint seed/index, etc.; fetches data from CSFloat with your API key; caches responses; and displays a clean list with core item details.

## Architecture
- Backend: FastAPI service that proxies and normalizes CSFloat requests.
  - Endpoints: `GET /api/listings`, `GET /api/item-names`
  - Caching: In-memory with 5-minute TTL for both listings and item names
  - Files: `backend/main.py`, `backend/api.py`, `backend/models.py`, `backend/utils.py`
- Frontend: Streamlit app that builds filters, calls the backend, and renders results.
  - Files: `frontend/app.py`, `frontend/api_client.py`, `frontend/components/*`, `frontend/config.py`, `frontend/models.py`

## Key Features
- Filters: limit, sort, category, def_index, float range, rarity, paint seed/index, user, collection, price range, type, stickers, item/market hash name.
- Names endpoint: Efficiently fetches distinct item names for search/selection.
- Caching: Reduces API calls and latency (backend cache + Streamlit cache).
- Resilience: Timeouts and structured logging on the backend; user-friendly error mapping on the frontend.

## Prerequisites
- Python 3.10+ recommended
- A valid CSFloat API key

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Provide your CSFloat API key (choose one of the two)
export CSFLOAT_API_KEY="<your_key>"
# or create backend/.env with:
# CSFLOAT_API_KEY=<your_key>

uvicorn backend.main:app --reload
# OpenAPI docs: http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Point to your backend (default is http://localhost:8000)
export API_BASE_URL="http://localhost:8000"
# or create frontend/.env with:
# API_BASE_URL=http://localhost:8000

streamlit run app.py
```

## Configuration
- Backend environment
  - `CSFLOAT_API_KEY`: Required. Your CSFloat API token.
- Frontend environment
  - `API_BASE_URL`: Optional. Defaults to `http://localhost:8000`.

Important: Do not commit API keys or secrets to version control. Keep `.env` files local and private.

## Backend API
- `GET /api/listings`
  - Description: Proxies CSFloat listings with normalized shape `{ data: [...], cursor: <str|null> }`.
  - Common query params:
    - `limit` (1–50), `sort_by`, `category`, `def_index` (repeatable), `min_float`, `max_float`, `rarity` (comma-separated),
      `paint_seed` (repeatable), `paint_index`, `user_id`, `collection`, `min_price`, `max_price`, `market_hash_name`, `item_name`, `type`, `stickers`.
    - For list-type params in direct calls, repeat the key: `...&paint_seed=1&paint_seed=2`.
  - Example:
    ```bash
    curl "http://localhost:8000/api/listings?limit=5&sort_by=best_deal&min_float=0.01&max_float=0.15"
    ```

- `GET /api/item-names`
  - Description: Returns a cached, alphabetized list of distinct item names.
  - Params: `limit` (1–200)
  - Example:
    ```bash
    curl "http://localhost:8000/api/item-names?limit=50"
    ```

## Frontend Usage
- Launch the Streamlit app, select filters in the sidebar, and click through results.
- The “Item Name” dropdown is powered by the `/api/item-names` endpoint and cached for 60 seconds client-side.

## Data Model (UI)
- `frontend/models.py` defines `ItemDTO` with: `name`, `price` (cents), `wear`, `rarity`, `float_value`.
- The UI merges nested `item` fields returned by the API and maps values into this DTO.

## Caching
- Backend: 5-minute in-memory cache keyed by query params; lightweight cache for names by limit.
- Frontend: Streamlit cache for listings and names with safe timeouts on network calls.

## Project Structure
```text
backend/
  api.py            # Routes: /api/listings, /api/item-names
  main.py           # App + CORS setup
  models.py         # Pydantic query models
  utils.py          # Env + logger helpers
  requirements.txt  # Backend deps
  .env              # Local-only env (not committed)
frontend/
  app.py            # Streamlit entry
  api_client.py     # HTTP calls to backend
  components/       # UI components (filters, item display, headers)
  config.py         # Frontend config + env
  models.py         # UI DTOs
  requirements.txt  # Frontend deps
  .env              # Local-only env (not committed)
```

## Troubleshooting
- 401 Unauthorized: Verify `CSFLOAT_API_KEY` is set and valid.
- 502 from backend: Upstream CSFloat error or timeout. Retry; check logs.
- Frontend cannot connect: Ensure backend is running and `API_BASE_URL` is correct.
- Empty results: Loosen filters (price/float/rarity) or increase `limit`.

## Roadmap (Suggestions)
- Add deal scoring (price vs market comps, float percentile, seed/sticker premiums).
- Add pagination UX (Load more) wired to the `cursor` param.
- Add retries/backoff on 429/5xx with jitter.
- Return typed response models on the backend and unit tests for parsing.
- Consolidate duplicated item display code and add thumbnails/links.
