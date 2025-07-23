import pandas as pd
import random

from shared.constants import (
    ROLE_VENDOR_MODEL_MAP,
    INVENTORY_MODEL_FAILURE_PROBS,
    IPAM_REGION_FAILURE_PROBS,
    DEFAULT_MODEL_FAILURE_PROB,
    DEFAULT_REGION_FAILURE_PROB
)

INPUT_FILE = "base_asset_dataset.csv"
OUTPUT_FILE = "labeled_asset_dataset.csv"

# --- Flatten unique model list from ROLE_VENDOR_MODEL_MAP ---
reference_models = set(model for models in ROLE_VENDOR_MODEL_MAP.values() for _, model in models)

# --- Ensure all reference models are represented ---
for model in reference_models:
    if model not in INVENTORY_MODEL_FAILURE_PROBS:
        INVENTORY_MODEL_FAILURE_PROBS[model] = DEFAULT_MODEL_FAILURE_PROB
        print(f"⚠️ Added missing model '{model}' to failure map with default probability {DEFAULT_MODEL_FAILURE_PROB}")

# --- Utility ---
def should_be_present(probability: float) -> int:
    return 1 if random.random() > probability else 0

# --- Load Dataset ---
df = pd.read_csv(INPUT_FILE)

# --- Inject Presence Flags ---
df["present_in_ipam"] = df["region"].apply(
    lambda r: should_be_present(IPAM_REGION_FAILURE_PROBS.get(r, DEFAULT_REGION_FAILURE_PROB))
)

df["present_in_inventory"] = df["model"].apply(
    lambda m: should_be_present(INVENTORY_MODEL_FAILURE_PROBS[m])
)

# --- Save Updated Dataset ---
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Labeled dataset with presence flags written to: {OUTPUT_FILE}")