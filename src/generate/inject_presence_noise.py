import os
import pandas as pd
import numpy as np
import argparse
import logging

from src.shared.constants import (
    ROLE_VENDOR_MODEL_MAP,
    INVENTORY_MODEL_MISSING_PROBS,
    IPAM_REGION_MISSING_PROBS,
    DEFAULT_MODEL_FAILURE_PROB
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)


def inject_noise(input_path: str, output_path: str, seed: int = 42):
    logging.info("🔄 Loading base dataset...")
    df = pd.read_csv(input_path)

    # --- Inventory Presence Flags ---
    df["missing_in_inventory"] = 0

    for model, failure_rate in INVENTORY_MODEL_MISSING_PROBS.items():
        idx = df["model"] == model
        n = idx.sum()
        n_fail = int(n * failure_rate)

        if n_fail > 0:
            fail_indices = df[idx].sample(n=n_fail, random_state=seed).index
            df.loc[fail_indices, "missing_in_inventory"] = 1

    # Fallback for unlisted models
    reference_models = set(model for models in ROLE_VENDOR_MODEL_MAP.values() for _, model in models)
    for model in reference_models:
        if model not in INVENTORY_MODEL_MISSING_PROBS:
            logging.warning(f"⚠️ Model {model} not in INVENTORY_MODEL_MISSING_PROBS — using default {DEFAULT_MODEL_FAILURE_PROB}")
            idx = df["model"] == model
            n = idx.sum()
            n_fail = int(n * DEFAULT_MODEL_FAILURE_PROB)
            if n_fail > 0:
                fail_indices = df[idx].sample(n=n_fail, random_state=seed).index
                df.loc[fail_indices, "missing_in_inventory"] = 1

    # --- IPAM Presence Flags ---
    df["missing_in_ipam"] = 0

    for region, failure_rate in IPAM_REGION_MISSING_PROBS.items():
        idx = df["region"] == region
        n = idx.sum()
        n_fail = int(n * failure_rate)

        if n_fail > 0:
            fail_indices = df[idx].sample(n=n_fail, random_state=seed).index
            df.loc[fail_indices, "missing_in_ipam"] = 1

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logging.info(f"✅ Labeled dataset saved to: {output_path}")
    logging.info(f"🧮 Final shape: {df.shape}")


def main():
    parser = argparse.ArgumentParser(description="Inject missing labels into asset dataset")
    parser.add_argument(
        "--input", type=str, default="data/raw/base_asset_dataset.csv",
        help="Path to base asset CSV file"
    )
    parser.add_argument(
        "--output", type=str, default="data/raw/labeled_asset_dataset.csv",
        help="Path to output labeled dataset"
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility"
    )
    args = parser.parse_args()

    inject_noise(args.input, args.output, args.seed)


if __name__ == "__main__":
    main()