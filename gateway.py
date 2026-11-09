import os

import httpx
from fastapi import FastAPI, HTTPException

from inference_client import send_inference
from schemas import InferenceRequest

app = FastAPI()


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/infer")
def infer(request: InferenceRequest):
    url = os.getenv("GATEWAY_UPSTREAM_URL")
    if not url:
        raise HTTPException(status_code=503, detail="Model endpoint is not configured")
    try:
        with httpx.Client() as model_client:
            return send_inference(model_client, url, request)
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Model request timed out") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail="Model service returned an error"
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503, detail="Model service is unavailable"
        ) from exc
