FROM python:3.13-slim
WORKDIR /app
ENV PORT=8501
ENV ADDRESS=0.0.0.0
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN apt-get update && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD streamlit run main.py --server.port=${PORT} --server.address=${ADDRESS}