# src/report/main.py

import argparse
import os
from src.report.generate_inventory_report import generate_inventory_report
from src.report.generate_ipam_report import generate_ipam_report

def main():
    parser = argparse.ArgumentParser(description="Generate ML model performance reports.")
    parser.add_argument(
        "--input_dir", type=str, default="data/processed",
        help="Directory containing the training datasets (CSV)"
    )
    parser.add_argument(
        "--model_dir", type=str, default="models",
        help="Directory containing the trained model artifacts"
    )
    parser.add_argument(
        "--output_dir", type=str, default="reports",
        help="Directory to write out report artifacts"
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Inventory report
    generate_inventory_report(
        model_path=os.path.join(args.model_dir, "inventory_model.pkl"),
        dataset_path=os.path.join(args.input_dir, "inventory_training_set.csv"),
        output_dir=os.path.join(args.output_dir, "inventory")
    )

    # IPAM report
    generate_ipam_report(
        model_path=os.path.join(args.model_dir, "ipam_model.pkl"),
        dataset_path=os.path.join(args.input_dir, "ipam_training_set.csv"),
        output_dir=os.path.join(args.output_dir, "ipam")
    )

if __name__ == "__main__":
    main()