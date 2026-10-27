from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    model: str = Field(min_length=1, max_length=100)
    prompt: str = Field(min_length=1, max_length=2000)
