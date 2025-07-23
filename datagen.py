import random
import pandas as pd
from faker import Faker

# Initialize Faker and constants
fake = Faker()

NUM_ASSETS = 10000

VENDOR_MODEL_WEIGHTED = {
    "Cisco": [("ISR4431", 0.7), ("NCS540", 0.3)],
    "Juniper": [("MX204", 0.9), ("QFX5120", 0.1)],
    "Arista": [("7280R", 1.0)],
    "Nokia": [("7750 SR-1", 1.0)],
    "ADVA": [("FSP150", 0.5), ("FSP3000", 0.5)],
    "RAD": [("ETX-2", 1.0)]
}

REGION_WEIGHTS = {
    "central": 0.1,
    "east": 0.1,
    "west": 0.2,
    "southeast": 0.05,
    "southwest": 0.05,
    "northeast": 0.25,
    "northwest": 0.25
}

OBS_STATUS_VALUES = ["active", "down", "degraded", "retired"]

# Weighted choice utility
def weighted_choice(choices):
    values, weights = zip(*choices)
    return random.choices(values, weights=weights, k=1)[0]

# Generator for one row
def generate_asset_row():
    hostname = fake.hostname().split('.')[0].replace('-', '')
    region = random.choices(list(REGION_WEIGHTS.keys()), weights=REGION_WEIGHTS.values(), k=1)[0]
    fqdn = f"{hostname}.{region}.lightspeed.net"
    ip_address = fake.ipv4()
    status = random.choice(OBS_STATUS_VALUES)
    vendor = random.choice(list(VENDOR_MODEL_WEIGHTED.keys()))
    model = weighted_choice(VENDOR_MODEL_WEIGHTED[vendor])
    
    return {
        "ip_address": ip_address,
        "hostname": hostname,
        "fqdn": fqdn,
        "region": region,
        "status": status,
        "vendor": vendor,
        "model": model
    }

# Generate and save to CSV
df = pd.DataFrame(generate_asset_row() for _ in range(NUM_ASSETS))
df.to_csv("base_asset_dataset.csv", index=False)