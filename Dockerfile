FROM python:3.11-slim

WORKDIR /app
RUN pip install --no-cache-dir google-genai

COPY arbiter.py .
RUN chmod +x arbiter.py

ENTRYPOINT ["python", "/app/arbiter.py"]
