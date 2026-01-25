import psycopg
import time
from datebase import get_conn

def init_db():
    for i in range(10):
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS system_metrics (
                            cpu_usage FLOAT NOT NULL,
                            ram_usage FLOAT NOT NULL,
                            load_average FLOAT NOT NULL,
                            network_bandwidth FLOAT NOT NULL,
                            created_at TIMESTAMPTZ DEFAULT NOW()
                        );
                    """)
                    print("Table created successfully!")
                return 
        except psycopg.OperationalError:
            print(f"Database not ready... (attempt {i+1}/10)")
            time.sleep(2)

if __name__ == "__main__":
    init_db()