from schemas import InferenceRequest


def build_payload(request: InferenceRequest) -> dict:
    return {
        "model": request.model,
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": False,
        "max_tokens": 64,
    }
