import fastapi
import uvicorn
import os
import schedule
import time
import threading
import logging

from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from pydantic import BaseModel
from datetime import datetime
from typing import List

from backend.db.database import get_conn, get_name
from backend.db.setup_db import init_db
from backend.db.logger import job


def run_logger():
    logging.info("Background logger started...")
    job()
    schedule.every(30).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # not to get into infinite while loop while testing
    if os.getenv("TESTING"):
        yield
        return
    init_db()
    # set up logger in daemon thread
    logger_thread = threading.Thread(target=run_logger, daemon=True)
    logger_thread.start()

    yield

    logging.info("Shutting down...")


class Metric(BaseModel):
    timestamp: datetime
    cpu_usage: float
    ram_usage: float
    load_average: float
    network_bandwidth: float


class MetricRangeResponse(BaseModel):
    data: List[Metric]


app = fastapi.FastAPI(
    title="Metrics API",
    description="API for getting metrics from database",
    version="1.0.0",
    lifespan=lifespan,
)

load_dotenv()
host = os.getenv("API_HOST", "0.0.0.0")
port = os.getenv("API_PORT", 8000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/metrics",
    summary="Last metric",
    description="Returns last entry from database",
    response_model=Metric,
)
def get_metrics():
    name = get_name()
    query = f"""
                SELECT timestamp, cpu_usage, ram_usage, load_average, network_bandwidth FROM {name} 
                ORDER BY timestamp 
                DESC LIMIT 1
            """
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                r = cur.fetchone()
                if not r:
                    raise fastapi.HTTPException(404, "No data")
                return {
                    "timestamp": r["timestamp"],
                    "cpu_usage": r["cpu_usage"],
                    "ram_usage": r["ram_usage"],
                    "load_average": r["load_average"],
                    "network_bandwidth": r["network_bandwidth"],
                }
    except Exception as e:
        logging.error(f"Database error: {e}")
        raise fastapi.HTTPException(500, detail=str(e))


@app.get(
    "/metrics/range",
    summary="Metrics from a period",
    description="Returns metrics from start to end",
    response_model=MetricRangeResponse,
)
def get_metrics_range(start: str, end: str):
    table = get_name()
    query = f"SELECT * FROM {table} WHERE timestamp BETWEEN %s AND %s ORDER BY timestamp ASC"
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (start, end))
                rows = cursor.fetchall()

                return {
                    "data": [
                        {
                            "timestamp": r["timestamp"],
                            "cpu_usage": r["cpu_usage"],
                            "ram_usage": r["ram_usage"],
                            "load_average": r["load_average"],
                            "network_bandwidth": r["network_bandwidth"],
                        }
                        for r in rows
                    ]
                }
    except Exception as e:
        logging.error(f"Database error: {e}")
        return {"data": []}


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host=host, port=port)
