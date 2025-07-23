import pandas as pd
import random

INPUT_FILE = "base_asset_dataset.csv"
OUTPUT_FILE = "labeled_asset_dataset.csv"

# Failure probabilities
IPAM_REGION_FAILURE_PROBS = {
    "northeast": 0.3,
    "northwest": 0.3,
    "central": 0.1,
    "east": 0.1,
    "west": 0.05,
    "southeast": 0.05,
    "southwest": 0.05
}

INVENTORY_MODEL_FAILURE_PROBS = {
    "MX204": 0.4,
    "QFX5120": 0.4,
    "ISR4431": 0.15,
    "NCS540": 0.15,
    "7280R": 0.05,
    "7750 SR-1": 0.1,
    "FSP150": 0.05,
    "FSP3000": 0.05,
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