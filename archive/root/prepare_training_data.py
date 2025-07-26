import os
import sqlite3
import pandas as pd

DB_FILE = os.path.join("synth", "sqlite", "d502_assets.db")
OUTPUT_DIR = "train_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load from SQLite
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM lightspeed_asset", conn)
conn.close()

# Inventory training set
inventory_df = df[["lightspeed_asset_id", "vendor", "model", "missing_in_inventory"]].rename(
    columns={"lightspeed_asset_id": "asset_id"}
)
inventory_df.to_csv(os.path.join(OUTPUT_DIR, "inventory_training_set.csv"), index=False)

# IPAM training set
ipam_df = df[["lightspeed_asset_id", "region", "missing_in_ipam"]].rename(
    columns={"lightspeed_asset_id": "asset_id"}
)
ipam_df.to_csv(os.path.join(OUTPUT_DIR, "ipam_training_set.csv"), index=False)

print("✅ Training datasets written to train_data/")
