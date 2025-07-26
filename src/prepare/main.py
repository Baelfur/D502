import argparse
from src.prepare.generate_lightspeed_asset import generate_lightspeed_asset
from src.prepare.prepare_inventory_training_set import generate_inventory_training_set
from src.prepare.prepare_ipam_training_set import generate_ipam_training_set

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

    # Step 1: Build lightspeed_asset table
    generate_lightspeed_asset(sqlite_path=args.sqlite_path)

    # Step 2: Prepare training sets
    generate_inventory_training_set(sqlite_path=args.sqlite_path, output_dir=args.output_dir)
    generate_ipam_training_set(sqlite_path=args.sqlite_path, output_dir=args.output_dir)

if __name__ == "__main__":
    main()