import psycopg
from psycopg.rows import dict_row
import os

DB_URL = f"host={os.getenv('DB_HOST')} dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASS')}"

def get_conn():
    return psycopg.connect(DB_URL, row_factory=dict_row)