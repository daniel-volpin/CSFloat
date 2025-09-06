
# CSFloat — Listings Explorer

## Quick Start

### Prerequisites
- Python 3.10+ recommended
- CSFloat API key

### Backend Setup
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set your CSFloat API key
export CSFLOAT_API_KEY="<your_key>"
# Or create backend/.env with:
# CSFLOAT_API_KEY=<your_key>

uvicorn backend.main:app --reload
# Docs: http://localhost:8000/docs
```

### Frontend Setup
```bash
cd frontend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set backend URL (default: http://localhost:8000)
export API_BASE_URL="http://localhost:8000"
# Or create frontend/.env with:
# API_BASE_URL=http://localhost:8000

streamlit run app.py
```

### Notes
- Do not commit API keys or secrets.
- Backend must be running before starting the frontend.
