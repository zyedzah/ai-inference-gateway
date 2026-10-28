from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class InferenceRequest(BaseModel):
    model: str = Field(min_length=1, max_length=100)
    prompt: str = Field(min_length=1, max_length=2000)


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/infer")
def infer(request: InferenceRequest):
    return {"status": "validated", "model": request.model}
