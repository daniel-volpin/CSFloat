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
- [Testing](#testing)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [API](#api-reference)
- [Troubleshooting](#troubleshooting)

## About the Project

Two-tier app: Streamlit frontend calls a small FastAPI service that standardizes responses and hosts AI-assisted analysis.

## Features

- Filter listings by price, float, rarity, and more.
- AI insights over the currently loaded items (backend-only OpenAI).
- Consistent error JSON and friendly UI messages.

## Getting Started

Quick, minimal setup (Python 3.11):

Prerequisites:

- Python 3.11 and pip
- Optional: Conda (for managing the env)
- Optional: GNU Make (for convenience targets)

```bash
# Create and activate env (conda example)
conda create -n csfloat python=3.11 -y && conda activate csfloat

# Install runtime deps (backend + frontend)
make install

# Optional: dev/test tooling
make dev-install

# No make? Use pip instead
pip install -r backend/requirements.txt -r frontend/requirements.txt
pip install -r requirements-dev.txt && pre-commit install

# Configure env files (copy examples and edit as needed)
cp backend/.env.example backend/.env   # set CSFLOAT/OPENAI keys
cp frontend/.env.example frontend/.env # API_BASE_URL defaults to http://localhost:8000
```

## Running

Open two terminals (env: `csfloat`):

- Backend: `uvicorn backend.main:app --reload` (docs: <http://localhost:8000/docs>)
- Frontend: `cd frontend && streamlit run app.py`

Non-dev CORS configuration:

- In staging/production, restrict CORS via `backend/.env`:

  - `CORS_ALLOW_ORIGINS=http://localhost:8501,https://yourdomain.com`
  - `CORS_ALLOW_CREDENTIALS=true`

  You can also use a JSON list:

  - `CORS_ALLOW_ORIGINS=["http://localhost:8501", "https://yourdomain.com"]`

  By default in dev, CORS is open (`*`).

## Testing

Run tests from the repo root (no external services required):

```bash
pytest -q
```

CI runs lint, type-checks, and tests on every push/PR.

## Configuration

- backend/.env
  - `CSFLOAT_API_KEY`: CSFloat API key (required for listings and item-names)
  - `OPENAI_API_KEY`: OpenAI key (required only for AI analysis)
  - `CORS_ALLOW_ORIGINS`: Comma-separated or JSON list of allowed origins (default `*`)
  - `CORS_ALLOW_CREDENTIALS`: `true/false` for credentials (default `true`)
- frontend/.env
  - `API_BASE_URL`: Defaults to `http://localhost:8000`

Note: AI analysis is optional. If `OPENAI_API_KEY` is not set, the rest of the app still works.

## Project Structure

```
backend/   # FastAPI service (routes, services, config)
frontend/  # Streamlit app (UI, client, models)
tests/     # Pytest suite (unit + API)
Makefile   # Common tasks (install, dev-install, run)
requirements-dev.txt  # Dev/test tooling
```

## Development

- Install dev tooling: `make dev-install`
- Update hooks: `pre-commit autoupdate`
- Run all checks locally: `pre-commit run --all-files`

## API Reference

- `GET /api/ping` — health check
- `GET /api/listings` — returns `{ data: ItemDTO[] }`
- `GET /api/item-names` — returns `{ names: string[] }`
- `POST /api/analyze` — `{ question, items, model?, max_items? } -> { result }`

Errors use `{ error, message, details? }`. Upstream CSFloat or model provider failures are mapped to appropriate HTTP status codes (e.g., 503 for upstream unavailability, 401 for model auth issues).

## Troubleshooting

- Cannot reach backend: verify it runs and `API_BASE_URL` is correct.
- `503` on listings/names: the upstream CSFloat API may be unavailable or rate limited; verify your `CSFLOAT_API_KEY` and try again.
- AI errors: ensure `OPENAI_API_KEY` is set (backend).

[⬆️ Back to top](#csfloat--listings-explorer)
