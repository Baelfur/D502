# src/prepare/prepare_inventory_training_set.py

import os
import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def generate_inventory_training_set(sqlite_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(sqlite_path)
    df = pd.read_sql("SELECT * FROM lightspeed_asset", conn)
    conn.close()

    # Filter down to only inventory features + label
    fields = ["region", "status", "vendor", "model", "missing_in_inventory"]
    if not all(col in df.columns for col in fields):
        missing = list(set(fields) - set(df.columns))
        raise ValueError(f"Missing required fields in lightspeed_asset: {missing}")

    inventory_df = df[fields].copy()
    output_path = os.path.join(output_dir, "inventory_training_set.csv")
    inventory_df.to_csv(output_path, index=False)

    logging.info(f"✅ Saved inventory training set: {output_path}")