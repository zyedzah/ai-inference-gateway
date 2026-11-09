import httpx
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from gateway import InferenceRequest, app
from inference_client import send_inference
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


def test_infer_valid(monkeypatch):
    monkeypatch.setenv(
        "GATEWAY_UPSTREAM_URL", "https://model._client/v1/chat/completions"
    )

    def fake_send(model_client, url, request):
        return {"answer": "Hello"}

    monkeypatch.setattr("gateway.send_inference", fake_send)
    response = client.post(
        "/infer",
        json={"model": "mistral", "prompt": "Hello"},
    )
    assert response.status_code == 200
    assert response.json() == {"answer": "Hello"}


def test_infer_upstream_error(monkeypatch):
    monkeypatch.setenv(
        "GATEWAY_UPSTREAM_URL", "https://model._client/v1/chat/completions"
    )

    def fake_send(model_client, url, request):
        reply = httpx.Response(500, request=httpx.Request("POST", url))
        reply.raise_for_status()

    monkeypatch.setattr("gateway.send_inference", fake_send)
    response = client.post(
        "/infer",
        json={"model": "mistral", "prompt": "Hello"},
    )
    assert response.status_code == 502
    assert response.json() == {"detail": "Model service returned an error"}


def test_infer_timeout(monkeypatch):
    monkeypatch.setenv(
        "GATEWAY_UPSTREAM_URL", "https://model._client/v1/chat/completions"
    )

    def fake_send(model_client, url, request):
        raise httpx.ReadTimeout("Simulated timeout")

    monkeypatch.setattr("gateway.send_inference", fake_send)
    response = client.post(
        "/infer",
        json={"model": "mistral", "prompt": "Hello"},
    )
    assert response.status_code == 504
    assert response.json() == {"detail": "Model request timed out"}


def test_infer_empty_prompt():
    response = client.post(
        "/infer",
        json={"model": "mistral", "prompt": ""},
    )
    assert response.status_code == 422


def test_negative_latency():
    with pytest.raises(ValidationError):
        InferenceResponse(model="llama3", response="Valid response.", latency_ms=-1)


def test_send_inference():
    def fake_model(outgoing):
        assert outgoing.method == "POST"
        return httpx.Response(200, json={"answer": "Hello"})

    request = InferenceRequest(model="mistral", prompt="Hello")

    with httpx.Client(transport=httpx.MockTransport(fake_model)) as client:
        result = send_inference(
            client, "https://model.test/v1/chat/completions", request
        )

    assert result == {"answer": "Hello"}
