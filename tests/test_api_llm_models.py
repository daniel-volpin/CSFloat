from fastapi.testclient import TestClient

from backend.main import app


def test_llm_models_endpoint_basic():
    client = TestClient(app)
    resp = client.get("/api/llm/models")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert isinstance(data.get("models"), list)
    # Ensure list is present and correctly formatted
    assert len(data["models"]) >= 1
    first = data["models"][0]
    assert "label" in first and "value" in first
    assert isinstance(first["label"], str)
    assert isinstance(first["value"], str)
    # First item should be a valid provider (lmstudio or openai)
    assert first["value"].startswith(("lmstudio:", "openai:"))
    # And ensure OpenAI option exists in the list for fallback
    assert any(m.get("value", "").startswith("openai:") for m in data["models"])
