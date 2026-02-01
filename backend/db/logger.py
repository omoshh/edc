from backend.db.database import get_conn, get_name
import backend.utils as utils
from datetime import datetime
import logging


def job():
    cp_av = utils.get_cpu()
    mem = utils.get_mem()
    load_av = utils.get_average()
    network = utils.get_bandwidth()
    now = datetime.now()
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
            logging.info(
                f"Logged {now}: CPU {cp_av}%, RAM {mem}%, Load Average (1m) {load_av}, Network bandwidth {network}MBps"
            )
    except Exception as e:
        logging.error(f"Logging failed: {e}")
