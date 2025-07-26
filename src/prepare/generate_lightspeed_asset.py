#src/prepare/generate_lightspeed_asset.py

import os
import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def generate_lightspeed_asset(sqlite_path: str):
    conn = sqlite3.connect(sqlite_path)

    # --- Load root tables ---
    obs = pd.read_sql("SELECT * FROM observability", conn)
    inv = pd.read_sql("SELECT * FROM inventory", conn)
    ipam = pd.read_sql("SELECT * FROM ipam", conn)

    logging.info("🔗 Joining tables to form lightspeed_asset...")

    # --- Join with Inventory ---
    merged = obs.merge(
        inv,
        left_on=["obs_ip_address", "obs_hostname"],
        right_on=["inv_ip_address", "inv_hostname"],
        how="left"
    )
    merged["missing_in_inventory"] = merged["inv_asset_id"].isna().astype(int)

    # --- Join with IPAM ---
    merged = merged.merge(
        ipam,
        left_on=["obs_ip_address", "obs_fqdn"],
        right_on=["ipam_ip_address", "ipam_fqdn"],
        how="left"
    )
    merged["missing_in_ipam"] = merged["ipam_asset_id"].isna().astype(int)

    # --- Select and rename fields for lightspeed_asset ---
    output = merged[[
        "obs_ip_address", "obs_hostname", "obs_fqdn", "obs_status",
        "inv_vendor", "inv_model", "ipam_region",
        "missing_in_inventory", "missing_in_ipam"
    ]].copy()

    output.columns = [
        "ip_address", "hostname", "fqdn", "status",
        "vendor", "model", "region",
        "missing_in_inventory", "missing_in_ipam"
    ]
    output.insert(0, "lightspeed_asset_id", range(1, len(output) + 1))

    # --- Write to SQLite ---
    output.to_sql("lightspeed_asset", conn, if_exists="replace", index=False)
    conn.close()

    logging.info("✅ lightspeed_asset table written to SQLite")