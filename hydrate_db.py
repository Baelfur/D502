import pandas as pd
import sqlite3
import os

INPUT_FILE = "synth/data/labeled_asset_dataset.csv"
DB_FILE = "synth/sqlite/d502_assets.db"

os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
df = pd.read_csv(INPUT_FILE)

# Deduplicate and normalize each system

# --- Observability ---
observability = df[["ip_address", "hostname", "fqdn", "status"]].drop_duplicates().copy()
observability.columns = ["obs_ip_address", "obs_hostname", "obs_fqdn", "obs_status"]
observability.insert(0, "obs_asset_id", range(1, len(observability) + 1))

# --- Inventory ---
inventory = df[["ip_address", "hostname", "vendor", "model"]].drop_duplicates().copy()
inventory.columns = ["inv_ip_address", "inv_hostname", "inv_vendor", "inv_model"]
inventory.insert(0, "inv_asset_id", range(1, len(inventory) + 1))

# --- IPAM ---
ipam = df[["ip_address", "fqdn", "region"]].drop_duplicates().copy()
ipam.columns = ["ipam_ip_address", "ipam_fqdn", "ipam_region"]
ipam.insert(0, "ipam_asset_id", range(1, len(ipam) + 1))

# --- Labels ---
# Binary indicators: was the asset observed in that system
labels = df.copy()
labels.insert(0, "asset_id", range(1, len(labels) + 1))
labels = labels[["asset_id"]].copy()
labels["is_observed"] = 1  # everything in observability.csv is observed
labels["is_in_inventory"] = 1 - df["missing_in_inventory"]
labels["is_in_ipam"] = 1 - df["missing_in_ipam"]

# --- Load into SQLite ---
conn = sqlite3.connect(DB_FILE)
observability.to_sql("observability", conn, if_exists="replace", index=False)
inventory.to_sql("inventory", conn, if_exists="replace", index=False)
ipam.to_sql("ipam", conn, if_exists="replace", index=False)
labels.to_sql("labels", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

print(f"✅ All normalized tables written to: {DB_FILE}")