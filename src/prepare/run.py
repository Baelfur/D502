# src/prepare/run.py

import os
import logging

from src.prepare.sqlite_io import extract_table

TRAIN_DATA_DIR = "train_data"
DB_PATH = os.path.join("synth", "sqlite", "d502_assets.db")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run():
    logging.info("📊 Starting prepare step...")

    os.makedirs(TRAIN_DATA_DIR, exist_ok=True)

    # Extract and save inventory table
    logging.info("📥 Extracting inventory table...")
    inventory_df = extract_table(DB_PATH, "inventory")
    inventory_outfile = os.path.join(TRAIN_DATA_DIR, "inventory_training_set.csv")
    inventory_df.to_csv(inventory_outfile, index=False)
    logging.info(f"✅ Saved inventory training set to: {inventory_outfile}")

    # Extract and save ipam table
    logging.info("📥 Extracting ipam table...")
    ipam_df = extract_table(DB_PATH, "ipam")
    ipam_outfile = os.path.join(TRAIN_DATA_DIR, "ipam_training_set.csv")
    ipam_df.to_csv(ipam_outfile, index=False)
    logging.info(f"✅ Saved ipam training set to: {ipam_outfile}")

    logging.info("✅ Prepare step complete.")
