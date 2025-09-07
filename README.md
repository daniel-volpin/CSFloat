# CSFloat — Listings Explorer

[//]: # (readme-top)

[![CI](https://github.com/daniel-volpin/CSFloat/actions/workflows/ci.yml/badge.svg)](https://github.com/daniel-volpin/CSFloat/actions/workflows/ci.yml)
[![CodeQL](https://github.com/daniel-volpin/CSFloat/actions/workflows/codeql.yml/badge.svg)](https://github.com/daniel-volpin/CSFloat/actions/workflows/codeql.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org)

[Demo](#running) • [Docs](#api-reference) • [Issues](../../issues) • [PRs](../../pulls)

Discover and filter CS:GO/CS2 item listings with a Streamlit UI and a FastAPI backend. Optional AI analysis runs server-side.

## Table of Contents

- [About](#about-the-project)
- [Features](#features)
- [Getting Started](#getting-started)
- [Running](#running)
- [API](#api-reference)
- [Troubleshooting](#troubleshooting)

## About the Project

Two-tier app: Streamlit frontend calls a small FastAPI service that standardizes responses and hosts AI-assisted analysis.

## Features

- Filter listings by price, float, rarity, and more.
- AI insights over the currently loaded items (backend-only OpenAI).
- Consistent error JSON and friendly UI messages.

## Getting Started

Single conda env for both backend and frontend.

```bash
# Create env
conda create -n csfloat python=3.11 -y
conda activate csfloat

# Install deps
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Backend env (backend/.env)
printf "CSFLOAT_API_KEY=your_csfloat_key\nOPENAI_API_KEY=your_openai_key\n" > backend/.env
# Optional demo: echo "USE_DUMMY_DATA=true" >> backend/.env

# Frontend env (frontend/.env)
printf "API_BASE_URL=http://localhost:8000\n" > frontend/.env
```

## Running

Open two terminals (env: `csfloat`):

- Backend: `uvicorn backend.main:app --reload` (docs: <http://localhost:8000/docs>)
- Frontend: `cd frontend && streamlit run app.py`

## Development

Set up dev tooling and git hooks (Black, Ruff, Isort, Autoflake, Flake8, Mypy) using the Makefile:

```bash
make dev-install
```

Tips:

- Update hooks to latest: `pre-commit autoupdate`
- Run checks manually: `pre-commit run --all-files`

## API Reference

- `GET /api/ping` — health check
- `GET /api/listings` — returns `{ data: ItemDTO[] }`
- `GET /api/item-names` — returns `{ names: string[] }`
- `POST /api/analyze` — `{ question, items, model?, max_items? } -> { result }`

Errors use `{ error, message, details? }`. When `USE_DUMMY_DATA=false` and no real data source, listings/names return `503`.

## Troubleshooting

- Cannot reach backend: verify it runs and `API_BASE_URL` is correct.
- `503` on listings/names: start data source or set `USE_DUMMY_DATA=true`.
- AI errors: ensure `OPENAI_API_KEY` is set (backend).

[⬆️ Back to top](#csfloat--listings-explorer)
