FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      tesseract-ocr \
      tesseract-ocr-por \
      poppler-utils \
      ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir openai-whisper

WORKDIR /app
COPY app.py /app/app.py

EXPOSE 8091
CMD ["python", "/app/app.py"]
