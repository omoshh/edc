FROM python:3.13-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN apt-get update && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["streamlit", "run", "main.py"]