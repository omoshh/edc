import fastapi
from backend import utils
from .db.datebase import get_conn, get_name

app = fastapi.FastAPI()

@app.get("/metrics")
def get_metrics():
    cp_av = utils.get_cpu()
    mem = utils.get_mem()
    load_av = utils.get_average()
    network = utils.get_bandwidth()
    datetime = utils.get_now()

    return {
        "datetime": datetime,
        "cpu_usage": cp_av,
        "memory_usage": mem,
        "load_average": load_av,
        "network_bandwidth": network,
    }

@app.get("/metrics/range")
def get_metrics_range(start: str, end: str):
    table = get_name()
    conn = get_conn()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table} WHERE timestamp BETWEEN ? AND ?"
    cursor.execute(query, (start, end))
    
    data = cursor.fetchall()
    conn.close()
    
    return {"data": data}