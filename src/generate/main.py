import argparse
import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.generate.generate_base_assets import generate_assets
from src.generate.inject_presence_noise import inject_noise
from src.generate.hydrate_db import hydrate_sqlite_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

def main():
    parser = argparse.ArgumentParser(description="Run synthetic asset data generation pipeline.")
    parser.add_argument(
        "--num_assets", type=int, default=11246,
        help="Number of synthetic assets to generate"
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--raw_dir", type=str, default="data/raw",
        help="Directory for generated raw data"
    )
    parser.add_argument(
        "--sqlite_path", type=str, default="data/sqlite/d502_assets.db",
        help="Path to output SQLite DB"
    )
    args = parser.parse_args()

    os.makedirs(args.raw_dir, exist_ok=True)

    base_file = os.path.join(args.raw_dir, "base_asset_dataset.csv")
    labeled_file = os.path.join(args.raw_dir, "labeled_asset_dataset.csv")

    logging.info("🚀 Starting data generation pipeline...")
    generate_assets(args.num_assets, base_file)
    inject_noise(base_file, labeled_file, args.seed)
    hydrate_sqlite_db(labeled_file, args.sqlite_path)
    logging.info("🏁 Data generation pipeline completed.")


if __name__ == "__main__":
    main()