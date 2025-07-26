"""
Hydrate the core D502 database with normalized tables:
- observability
- inventory
- ipam

Only non-missing data is included for inventory and IPAM.
"""

import os
import sqlite3
import pandas as pd

# --- Config ---
INPUT_FILE = "synth/data/labeled_asset_dataset.csv"
DB_FILE = "synth/sqlite/d502_assets.db"
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

# --- Load dataset ---
df = pd.read_csv(INPUT_FILE)

# --- Observability ---
observability = (
    df[["ip_address", "hostname", "fqdn", "status"]]
    .drop_duplicates()
    .rename(columns={
        "ip_address": "obs_ip_address",
        "hostname": "obs_hostname",
        "fqdn": "obs_fqdn",
        "status": "obs_status"
    })
    .reset_index(drop=True)
)
observability.insert(0, "obs_asset_id", observability.index + 1)

# --- Inventory (non-missing only) ---
inventory = (
    df[df["missing_in_inventory"] == 0][["ip_address", "hostname", "vendor", "model"]]
    .drop_duplicates()
    .rename(columns={
        "ip_address": "inv_ip_address",
        "hostname": "inv_hostname",
        "vendor": "inv_vendor",
        "model": "inv_model"
    })
    .reset_index(drop=True)
)
inventory.insert(0, "inv_asset_id", inventory.index + 1)

# --- IPAM (non-missing only) ---
ipam = (
    df[df["missing_in_ipam"] == 0][["ip_address", "fqdn", "region"]]
    .drop_duplicates()
    .rename(columns={
        "ip_address": "ipam_ip_address",
        "fqdn": "ipam_fqdn",
        "region": "ipam_region"
    })
    .reset_index(drop=True)
)
ipam.insert(0, "ipam_asset_id", ipam.index + 1)

# --- Write to SQLite ---
with sqlite3.connect(DB_FILE) as conn:
    observability.to_sql("observability", conn, if_exists="replace", index=False)
    inventory.to_sql("inventory", conn, if_exists="replace", index=False)
    ipam.to_sql("ipam", conn, if_exists="replace", index=False)

print(f"✅ Hydration complete. Tables written to {DB_FILE}")