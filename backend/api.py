import fastapi
import uvicorn
import os
import schedule
import time
import threading

from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from db.database import get_conn, get_name
from db import setup_db
from db.logger import job

def run_logger():
    print("Background logger started...")
    job() 
    schedule.every(30).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    setup_db()
    # set up logger in daemon thread
    logger_thread = threading.Thread(target=run_logger, daemon=True)
    logger_thread.start()
    
    yield
    
    print("Shutting down...")

app = fastapi.FastAPI(lifespan=lifespan)

load_dotenv()
host = os.getenv('API_HOST', '0.0.0.0')
port = os.getenv('API_PORT', 8000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/metrics")
def get_metrics():
    name = get_name()
    query = f"""
                SELECT * FROM {name} 
                ORDER BY timestamp DESC 
                LIMIT 1
            """
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchone()
    except Exception as e:
        print(f"Database error: {e}")
        return None

@app.get("/metrics/range")
def get_metrics_range(start: str, end: str):
    table = get_name()
    query = f"SELECT * FROM {table} WHERE timestamp BETWEEN %s AND %s ORDER BY timestamp ASC"
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (start, end))
                data = cursor.fetchall()
                return {"data": data}
    except Exception as e:
        print(f"Database error: {e}")
        return None

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)