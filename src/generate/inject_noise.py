import pandas as pd
import numpy as np
import os
from synth.shared.constants import (
    ROLE_VENDOR_MODEL_MAP,
    INVENTORY_MODEL_MISSING_PROBS,
    IPAM_REGION_MISSING_PROBS,
    DEFAULT_MODEL_FAILURE_PROB,
)

def inject_noise(df):
    df["missing_in_inventory"] = 0

    for model, rate in INVENTORY_MODEL_MISSING_PROBS.items():
        idx = df["model"] == model
        n_fail = int(idx.sum() * rate)
        if n_fail > 0:
            df.loc[df[idx].sample(n=n_fail, random_state=42).index, "missing_in_inventory"] = 1

    reference_models = {model for pairs in ROLE_VENDOR_MODEL_MAP.values() for _, model in pairs}
    for model in reference_models:
        if model not in INVENTORY_MODEL_MISSING_PROBS:
            idx = df["model"] == model
            n_fail = int(idx.sum() * DEFAULT_MODEL_FAILURE_PROB)
            if n_fail > 0:
                df.loc[df[idx].sample(n=n_fail, random_state=42).index, "missing_in_inventory"] = 1

    df["missing_in_ipam"] = 0
    for region, rate in IPAM_REGION_MISSING_PROBS.items():
        idx = df["region"] == region
        n_fail = int(idx.sum() * rate)
        if n_fail > 0:
            df.loc[df[idx].sample(n=n_fail, random_state=42).index, "missing_in_ipam"] = 1

    output_path = os.path.join("train_data", "labeled_asset_dataset.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Risk-labeled dataset written to: {output_path}")
    return df