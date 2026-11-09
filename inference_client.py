import httpx

from schemas import InferenceRequest


def build_payload(request: InferenceRequest) -> dict:
    return {
        "model": request.model,
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": False,
        "max_tokens": 64,
    }


def send_inference(client: httpx.Client, url: str, request: InferenceRequest) -> dict:
    payload = build_payload(request)
    response = client.post(url, json=payload, timeout=15.0)
    response.raise_for_status()
    return response.json()
