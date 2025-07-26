# src/prepare/main.py

import argparse
from src.prepare.prepare_training_data import prepare_training_sets

def parse_args():
    parser = argparse.ArgumentParser(description="Prepare training datasets from hydrated SQLite DB")
    parser.add_argument(
        "--sqlite_path",
        type=str,
        required=True,
        help="Path to SQLite database file (e.g. data/sqlite/d502_assets.db)",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="data/processed",
        help="Directory to save training datasets",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    prepare_training_sets(args.sqlite_path, args.output_dir)

if __name__ == "__main__":
    main()