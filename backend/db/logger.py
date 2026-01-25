from datebase import get_conn
from backend import utils
import schedule
import time
from datetime import datetime

def job():
    cp_av = utils.get_cpu()
    mem = utils.get_mem()
    load_av = utils.get_average()
    network = utils.get_bandwidth()
    now = datetime.now()
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO system_metrics (cpu_usage, ram_usage, load_average, network_bandwidth, created_at) VALUES (%s, %s, %s, %s, %s)",
                    (cp_av, mem, load_av, network, now)
                )
            conn.commit()
            print(f"Logged {now}: CPU {cp_av}%, RAM {mem}%, Load Average (1m) {load_av}%, Network bendwidth {network}MBps") 
    except Exception as e:
        print(f"Logging failed: {e}")
    
print("logger starting... waiting for first minute")
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)