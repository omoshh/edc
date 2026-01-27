FROM python:3.13-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN apt-get update && pip install --no-cache-dir -r requirements.txt && rm -rf /var/lib/apt/lists/*
COPY . .
CMD ["python", "api.py"]