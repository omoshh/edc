import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

load_dotenv()
VARS = {
    "db_user": os.getenv('DB_USER', 'postgres'),
    "db_pass": os.getenv('DB_PASS'),
    "db_host": os.getenv('DB_HOST', 'localhost'),
    "db_port": os.getenv('DB_PORT', '5432'),
    "db_name": os.getenv('DB_NAME', 'metrics')
}
DB_URL = f"postgresql://{VARS['db_user']}:{VARS['db_pass']}@{VARS['db_host']}:{VARS['db_port']}/{VARS['db_name']}"
def get_conn():
    return psycopg.connect(DB_URL, row_factory=dict_row)

def get_name():
    return os.getenv('DB_TABLE', 'system_metrics')