import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = f"host={os.getenv('DB_HOST')} dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASS')} port={os.getenv('DB_PORT')}"

def get_conn():
    return psycopg.connect(DB_URL, row_factory=dict_row)

def get_name():
    return os.getenv('DB_TABLE', 'system_metrics')