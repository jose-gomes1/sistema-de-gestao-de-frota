import sqlite3
from pathlib import Path
import os

IS_STREAMLIT = os.getenv("STREAMLIT_SERVER_RUNNING") == "1"

DB_DIR = Path("/mount/data") if IS_STREAMLIT else Path(__file__).parent
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "frota.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
