import sqlite3
from pathlib import Path
import streamlit as st

# Use Streamlit persistent storage
DB_DIR = Path("/mount/data")
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "frota.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
