# src/prepare/sqlite_io.py

import sqlite3
import pandas as pd

def extract_table(db_path: str, table_name: str) -> pd.DataFrame:
    """Extract a table from the SQLite database as a pandas DataFrame."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df