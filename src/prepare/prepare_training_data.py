import argparse
import os
import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

def prepare_training_sets(db_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)

    # --- Load Tables ---
    obs = pd.read_sql("SELECT * FROM observability", conn)
    inv = pd.read_sql("SELECT * FROM inventory", conn)
    ipam = pd.read_sql("SELECT * FROM ipam", conn)

    logging.info("🔗 Performing LEFT JOINs...")

    # --- Inventory Join ---
    inv_join = obs.merge(
        inv,
        left_on=["obs_ip_address", "obs_hostname"],
        right_on=["inv_ip_address", "inv_hostname"],
        how="left",
        suffixes=("", "_inv")
    )
    inv_join["missing_in_inventory"] = inv_join["inv_asset_id"].isna().astype(int)

    inv_out = inv_join[[
        "obs_ip_address", "obs_hostname", "obs_status",
        "inv_vendor", "inv_model", "missing_in_inventory"
    ]].copy()

    inventory_out_path = os.path.join(output_dir, "inventory_training_set.csv")
    inv_out.to_csv(inventory_out_path, index=False)
    logging.info(f"✅ Saved inventory training set: {inventory_out_path}")

    # --- IPAM Join ---
    ipam_join = obs.merge(
        ipam,
        left_on=["obs_ip_address", "obs_fqdn"],
        right_on=["ipam_ip_address", "ipam_fqdn"],
        how="left",
        suffixes=("", "_ipam")
    )
    ipam_join["missing_in_ipam"] = ipam_join["ipam_asset_id"].isna().astype(int)

    ipam_out = ipam_join[[
        "obs_ip_address", "obs_fqdn", "obs_status", "ipam_region", "missing_in_ipam"
    ]].copy()

    ipam_out_path = os.path.join(output_dir, "ipam_training_set.csv")
    ipam_out.to_csv(ipam_out_path, index=False)
    logging.info(f"✅ Saved IPAM training set: {ipam_out_path}")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Prepare training datasets from SQLite asset DB")
    parser.add_argument(
        "--db_path", type=str, default="data/sqlite/d502_assets.db",
        help="Path to the hydrated SQLite asset database"
    )
    parser.add_argument(
        "--output_dir", type=str, default="data/processed",
        help="Directory where training CSVs will be saved"
    )
    args = parser.parse_args()

    prepare_training_sets(args.db_path, args.output_dir)


if __name__ == "__main__":
    main()
