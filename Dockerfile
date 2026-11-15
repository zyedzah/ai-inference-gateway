FROM python:3.12-slim-bookworm
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY gateway.py inference_client.py schemas.py ./
USER 10001
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "8080"]
