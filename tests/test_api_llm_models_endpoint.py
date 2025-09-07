import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestLLMModelsAPI:
    def test_given_app_when_get_llm_models_then_return_valid_models_list(self, client):
        # Arrange

        # Act
        resp = client.get("/llm/models")

        # Assert
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert isinstance(data.get("models"), list)
        assert len(data["models"]) >= 1
        first = data["models"][0]
        assert "label" in first and "value" in first
        assert isinstance(first["label"], str)
        assert isinstance(first["value"], str)
        assert first["value"].startswith(("lmstudio:", "openai:"))
        assert any(m.get("value", "").startswith("openai:") for m in data["models"])
