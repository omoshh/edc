import fastapi
from backend import utils
from .db.database import get_conn, get_name

app = fastapi.FastAPI()

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
