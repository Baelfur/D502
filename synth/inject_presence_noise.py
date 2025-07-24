import pandas as pd
import numpy as np

from shared.constants import (
    ROLE_VENDOR_MODEL_MAP,
    INVENTORY_MODEL_FAILURE_PROBS,
    IPAM_REGION_FAILURE_PROBS,
    DEFAULT_MODEL_FAILURE_PROB
)

INPUT_FILE = "data/base_asset_dataset.csv"
OUTPUT_FILE = "data/labeled_asset_dataset.csv"

# Load data
df = pd.read_csv(INPUT_FILE)

# --- Inject INVENTORY failures deterministically per model ---
df["present_in_inventory"] = 1  # start with everything present

for model, failure_rate in INVENTORY_MODEL_FAILURE_PROBS.items():
    idx = df["model"] == model
    n = idx.sum()
    n_fail = int(n * failure_rate)
    
    if n_fail > 0:
        fail_indices = df[idx].sample(n=n_fail, random_state=42).index
        df.loc[fail_indices, "present_in_inventory"] = 0

# Ensure all models from ROLE_VENDOR_MODEL_MAP are represented
reference_models = set(model for models in ROLE_VENDOR_MODEL_MAP.values() for _, model in models)
for model in reference_models:
    if model not in INVENTORY_MODEL_FAILURE_PROBS:
        print(f"⚠️ WARNING: Model {model} missing from INVENTORY_MODEL_FAILURE_PROBS. Using default {DEFAULT_MODEL_FAILURE_PROB}.")
        idx = df["model"] == model
        n = idx.sum()
        n_fail = int(n * DEFAULT_MODEL_FAILURE_PROB)
        if n_fail > 0:
            fail_indices = df[idx].sample(n=n_fail, random_state=42).index
            df.loc[fail_indices, "present_in_inventory"] = 0

# --- Inject IPAM failures deterministically per region ---
df["present_in_ipam"] = 1  # start with everything present

for region, failure_rate in IPAM_REGION_FAILURE_PROBS.items():
    idx = df["region"] == region
    n = idx.sum()
    n_fail = int(n * failure_rate)

    if n_fail > 0:
        fail_indices = df[idx].sample(n=n_fail, random_state=42).index
        df.loc[fail_indices, "present_in_ipam"] = 0

# Save the updated dataset
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Labeled dataset written to: {OUTPUT_FILE}")