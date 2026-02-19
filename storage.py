import sqlite3
from pathlib import Path

# ÚNICO diretório com permissões de escrita no Streamlit Cloud
DB_PATH = Path("/tmp/frota.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

