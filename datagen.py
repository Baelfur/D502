import random
import pandas as pd
from faker import Faker

# Initialize Faker
fake = Faker()

# Configuration
NUM_ASSETS = 10_000

# Weighted vendor-model distribution
VENDOR_MODEL_WEIGHTED = {
    "Cisco": [("ISR4431", 0.7), ("NCS540", 0.3)],
    "Juniper": [("MX204", 0.9), ("QFX5120", 0.1)],
    "Arista": [("7280R", 1.0)],
    "Nokia": [("7750 SR-1", 1.0)],
    "ADVA": [("FSP150", 0.5), ("FSP3000", 0.5)],
    "RAD": [("ETX-2", 1.0)]
}

# Region weights
REGION_WEIGHTS = {
    "central": 0.1,
    "east": 0.1,
    "west": 0.2,
    "southeast": 0.05,
    "southwest": 0.05,
    "northeast": 0.25,
    "northwest": 0.25
}

# Region → site code map
REGION_SITE_MAP = {
    "central":    ["DAL", "AUS", "OKC"],
    "east":       ["ATL", "CLT", "PIT"],
    "west":       ["SEA", "LAX", "SFO"],
    "southeast":  ["MIA", "JAX", "BNA"],
    "southwest":  ["PHX", "ABQ", "ELP"],
    "northeast":  ["NYC", "BOS", "PHL"],
    "northwest":  ["POR", "GEG", "BOI"]
}

# Device roles → fixed 2-char codes
DEVICE_ROLE_CODES = {
    "edge": "ED",
    "core": "CO",
    "agg":  "AG",
    "dist": "DS",
    "rtr":  "RT",
    "sw":   "SW"
}

# Observability status values with weights
OBS_STATUS_WEIGHTED = [
    ("active", 0.7),
    ("degraded", 0.2),
    ("down", 0.07),
    ("retired", 0.03)
]

# Weighted choice helper
def weighted_choice(choices):
    values, weights = zip(*choices)
    return random.choices(values, weights=weights, k=1)[0]

# Generate hostname with fixed length and uppercase formatting
def generate_hostname(region: str) -> str:
    site_code = random.choice(REGION_SITE_MAP[region])
    role_name = random.choice(list(DEVICE_ROLE_CODES.keys()))
    role_code = DEVICE_ROLE_CODES[role_name]
    num = str(random.randint(1, 99)).zfill(2)
    return f"{site_code}{role_code}{num}"

def generate_asset_row():
    region = random.choices(list(REGION_WEIGHTS.keys()), weights=REGION_WEIGHTS.values(), k=1)[0]
    hostname = generate_hostname(region)
    fqdn = f"{hostname}.{region}.lightspeed.net"
    ip_address = fake.ipv4()
    status = weighted_choice(OBS_STATUS_WEIGHTED)  # uses new weighted distribution
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

# Generate the full dataset
df = pd.DataFrame(generate_asset_row() for _ in range(NUM_ASSETS))

# Save to file or inspect in memory
df.to_csv("base_asset_dataset.csv", index=False)