from .database import get_conn, get_name
from backend import utils
from datetime import datetime, timezone

def job():
    cp_av = utils.get_cpu()
    mem = utils.get_mem()
    load_av = utils.get_average()
    network = utils.get_bandwidth()
    now = datetime.now(timezone.utc)
    table_name = get_name()
    query = f"""
        INSERT INTO {table_name} 
        (cpu_usage, ram_usage, load_average, network_bandwidth, timestamp) 
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (cp_av, mem, load_av, network, now))
            conn.commit()
            print(f"Logged {now}: CPU {cp_av}%, RAM {mem}%, Load Average (1m) {load_av}, Network bandwidth {network}MBps") 
    except Exception as e:
        print(f"Logging failed: {e}")