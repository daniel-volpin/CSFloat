# CSFloat — Listings Explorer

## Overview
- A two-tier app to discover and filter CS:GO item listings for investing.
- Backend: FastAPI wrapper around CSFloat’s marketplace API with caching.
- Frontend: Streamlit UI for filtering and viewing items; includes an AI assistant to analyze the currently loaded listings.

## Architecture
- Backend
  - Routes: `GET /api/listings`, `GET /api/item-names`
  - Files: `backend/main.py`, `backend/api.py`, `backend/models.py`, `backend/utils.py`
  - Cache: In-memory, 5-minute TTL (listings + names)
- Frontend
  - Files: `frontend/app.py`, `frontend/api_client.py`, `frontend/components/*`, `frontend/config.py`, `frontend/models.py`, `frontend/llm_client.py`

## Prerequisites
- Python 3.10+
- CSFloat API key
- Optional: OpenAI API key for AI analysis

## Quick Start

### Backend (conda)
```bash
cd backend

# Option A: Use the provided environment.yml
conda env create -f environment.yml
conda activate csfloat-backend

# Option B: Create an env and install via pip
conda create -n csfloat-backend python=3.11 -y
conda activate csfloat-backend
pip install -r requirements.txt

# Provide your CSFloat API key
export CSFLOAT_API_KEY="<your_key>"
# or create backend/.env with:
# CSFLOAT_API_KEY=<your_key>

uvicorn backend.main:app --reload
# OpenAPI docs: http://localhost:8000/docs
```

### Frontend (conda)
```bash
cd frontend

# Option A: Use the provided environment.yml
conda env create -f environment.yml
conda activate csfloat-frontend

# Option B: Create an env and install via pip
conda create -n csfloat-frontend python=3.11 -y
conda activate csfloat-frontend
pip install -r requirements.txt

# Point to your backend (default is http://localhost:8000)
export API_BASE_URL="http://localhost:8000"
# or create frontend/.env with:
# API_BASE_URL=http://localhost:8000

streamlit run app.py
```

## Configuration
- Backend
  - `CSFLOAT_API_KEY` (required): Your CSFloat API token.
- Frontend
  - `API_BASE_URL` (optional): Defaults to `http://localhost:8000`.
  - AI:
    - OpenAI: `OPENAI_API_KEY` and optional `OPENAI_MODEL` (e.g., `gpt-4o`).
    - Optional: `OPENAI_BASE_URL` if proxying/self-hosting.

Use OpenAI directly
- Set `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`, default is `gpt-4o`).

Important: Do not commit API keys or secrets. Keep `.env` files private.
Tip (conda): To update envs after changing requirements, run `conda env update -f environment.yml` in each folder.

## Backend API
- `GET /api/listings`
  - Returns: `{ data: [...], cursor: <str|null> }`
  - Common query params: `limit` (1–50), `sort_by`, `category`, `def_index` (repeatable), `min_float`, `max_float`, `rarity` (comma-separated), `paint_seed` (repeatable), `paint_index`, `user_id`, `collection`, `min_price`, `max_price`, `market_hash_name`, `item_name`, `type`, `stickers`.
  - Example:
    ```bash
    curl "http://localhost:8000/api/listings?limit=5&sort_by=best_deal&min_float=0.01&max_float=0.15"
    ```
- `GET /api/item-names`
  - Returns: `{ names: ["AK-47 | Redline", ...] }`
  - Params: `limit` (1–200)
  - Example:
    ```bash
    curl "http://localhost:8000/api/item-names?limit=50"
    ```

## Using AI to Analyze Listings
This feature lets you ask an LLM about the listings already loaded in the UI (no external lookups).

1) Configure API access (OpenAI) via env vars in the Frontend section above.
2) In the Streamlit app, open “Ask AI about current listings”.
3) Enter a question (e.g., “Best low-float AKs under $200?”) and click “Analyze Listings with AI”.

Notes
- The app sends a concise digest per item: index, name, price, wear, rarity, float; you can control how many items are included.
- The model will recommend items by index/name with a short rationale; it does not fetch external prices.

## Troubleshooting
- 401 Unauthorized (backend): Verify `CSFLOAT_API_KEY`.
- 502 (backend): Upstream CSFloat error or timeout. Retry; check logs.
- Frontend can’t connect: Ensure backend is running and `API_BASE_URL` is correct.
- AI errors: Ensure `OPENAI_API_KEY` is set and the model exists.
- TypeError about `proxies` in OpenAI client: Update `httpx` to >= 0.27.0 in the frontend env:
  ```bash
  pip install -U httpx
  ```
