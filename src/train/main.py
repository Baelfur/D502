# src/train/main.py

import argparse
from src.train.train_inventory_model import train_inventory_model
from src.train.train_ipam_model import train_ipam_model

def parse_args():
    parser = argparse.ArgumentParser(description="Train inventory and IPAM models")
    parser.add_argument("--input_dir", type=str, default="data/processed", help="Directory with training CSVs")
    return parser.parse_args()

def main():
    args = parse_args()
    train_inventory_model(args.input_dir)
    train_ipam_model(args.input_dir)

if __name__ == "__main__":
    main()