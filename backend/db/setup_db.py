import psycopg
import time
from db.database import get_conn, get_name

def init_db():
    table_name = get_name()
    q = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                cpu_usage FLOAT NOT NULL,
                ram_usage FLOAT NOT NULL,
                load_average FLOAT NOT NULL,
                network_bandwidth FLOAT NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT NOW()
                );
        """
    for i in range(10):
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(q)
                    print("Table created successfully!")
                return 
        except psycopg.OperationalError:
            print(f"Database not ready... (attempt {i+1}/10)")
            time.sleep(2)

if __name__ == "__main__":
    init_db()