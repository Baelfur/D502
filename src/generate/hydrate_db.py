import os
import sqlite3
import pandas as pd
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)


def hydrate_sqlite_db(input_file: str, db_file: str):
    logging.info("🔄 Loading labeled dataset...")
    df = pd.read_csv(input_file)

    # --- Observability ---
    logging.info("📦 Building 'observability' table...")
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

    # --- Inventory ---
    logging.info("📦 Building 'inventory' table...")
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

    # --- IPAM ---
    logging.info("📦 Building 'ipam' table...")
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
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    with sqlite3.connect(db_file) as conn:
        observability.to_sql("observability", conn, if_exists="replace", index=False)
        inventory.to_sql("inventory", conn, if_exists="replace", index=False)
        ipam.to_sql("ipam", conn, if_exists="replace", index=False)

    logging.info(f"✅ Hydration complete. Tables written to {db_file}")


def main():
    parser = argparse.ArgumentParser(description="Hydrate SQLite database from labeled asset data")
    parser.add_argument(
        "--input", type=str, default="data/raw/labeled_asset_dataset.csv",
        help="Path to labeled asset dataset CSV"
    )
    parser.add_argument(
        "--output", type=str, default="data/sqlite/d502_assets.db",
        help="Path to SQLite database file"
    )
    args = parser.parse_args()

    hydrate_sqlite_db(args.input, args.output)


if __name__ == "__main__":
    main()
