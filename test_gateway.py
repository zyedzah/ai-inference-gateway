import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from gateway import InferenceRequest, app
from schemas import InferenceResponse

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_request():
    request = InferenceRequest(model="llama3", prompt="Hello")
    assert request.model == "llama3"
    assert request.prompt == "Hello"


def test_empty_prompt():
    with pytest.raises(ValidationError):
        InferenceRequest(model="llama3", prompt="")


def test_infer_valid():
    response = client.post(
        "/infer",
        json={"model": "mistral", "prompt": "Hello"},
    )
    assert response.status_code == 200
    assert response.json() == {"status": "validated", "model": "mistral"}


def test_infer_empty_prompt():
    response = client.post(
        "/infer",
        json={"model": "mistral", "prompt": ""},
    )
    assert response.status_code == 422


def test_negative_latency():
    with pytest.raises(ValidationError):
        InferenceResponse(model="llama3", response="Valid response.", latency_ms=-1)
