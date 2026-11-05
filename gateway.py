from fastapi import FastAPI

from schemas import InferenceRequest

app = FastAPI()


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/infer")
def infer(request: InferenceRequest):
    return {"status": "validated", "model": request.model}
