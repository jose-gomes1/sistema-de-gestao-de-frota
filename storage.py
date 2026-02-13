import sqlite3
from pathlib import Path
import os

# If /mount/data exists, use it (Streamlit Cloud)
if Path("/mount/data").exists():
    DB_DIR = Path("/mount/data")
else:
    DB_DIR = Path(__file__).parent

DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "frota.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
