import sqlite3
from pathlib import Path

# Streamlit Cloud persistent storage directory
DB_PATH = Path("/mount/data/frota.db")

def get_conn():
    # Ensure parent directory exists (safe, since /mount/data already exists)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
