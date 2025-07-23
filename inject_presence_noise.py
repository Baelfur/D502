import pandas as pd
import random

INPUT_FILE = "base_asset_dataset.csv"
OUTPUT_FILE = "labeled_asset_dataset.csv"

# Failure probabilities
IPAM_REGION_FAILURE_PROBS = {
    "northeast": 0.3,
    "northwest": 0.01,
    "central": 0.01,
    "east": 0.02,
    "west": 0.05,
    "southeast": 0.03,
    "southwest": 0.01
}

INVENTORY_MODEL_FAILURE_PROBS = {
    "MX204": 0.01,
    "QFX5120": 0.03,
    "ISR4431": 0.02,
    "NCS540": 0.7,
    "7280R": 0.01,
    "7750 SR-1": 0.01,
    "FSP150": 0.40,
    "FSP3000": 0.25,
    "ETX-2": 0.05
}

def should_be_present(probability: float) -> int:
    return 1 if random.random() > probability else 0

# Load base data
df = pd.read_csv(INPUT_FILE)

# Inject presence flags
df["present_in_ipam"] = df["region"].apply(
    lambda r: should_be_present(IPAM_REGION_FAILURE_PROBS.get(r, 0.1))
)

df["present_in_inventory"] = df["model"].apply(
    lambda m: should_be_present(INVENTORY_MODEL_FAILURE_PROBS.get(m, 0.1))
)

# Write updated dataset
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Noise-injected dataset written to: {OUTPUT_FILE}")