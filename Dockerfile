FROM python:3.12-slim-trixie
RUN apt-get update \
  && apt-get install -y --only-upgrade --no-install-recommends 'zlib1g=1:1.3.dfsg+really1.3.1-1+deb13u1' \
  && rm -rf /var/lib/apt/list/*
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY gateway.py inference_client.py schemas.py ./
USER 10001
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "8080"]
