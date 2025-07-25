import pandas as pd
import logging
import os
from .utils import generate_unique_asset_row

NUM_ASSETS = 11246
OUTPUT_FILE = "synth/sqlite/d502_assets.db"

def generate_base_assets():
    logging.info("📦 Generating base asset dataset...")
    rows = [generate_unique_asset_row() for _ in range(NUM_ASSETS)]
    df = pd.DataFrame(rows)

    os.makedirs("train_data", exist_ok=True)
    output_path = os.path.join("train_data", "base_asset_dataset.csv")
    df.to_csv(output_path, index=False)
    logging.info(f"✅ Saved base asset dataset to: {output_path}")

    return df