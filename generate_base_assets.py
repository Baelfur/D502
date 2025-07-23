import random
import pandas as pd
from faker import Faker
import ipaddress
import logging
import time

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

# --- Initialization ---
fake = Faker()
NUM_ASSETS = 10_000

# --- Configuration ---

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

SITE_STATE_MAP = {
    "DAL": "TX", "AUS": "TX", "OKC": "OK",
    "ATL": "GA", "CLT": "NC", "PIT": "PA",
    "SEA": "WA", "LAX": "CA", "SFO": "CA",
    "MIA": "FL", "JAX": "FL", "BNA": "TN",
    "PHX": "AZ", "ABQ": "NM", "ELP": "TX",
    "NYC": "NY", "BOS": "MA", "PHL": "PA",
    "POR": "OR", "GEG": "WA", "BOI": "ID"
}

REGION_SITE_MAP = {
    "central":    ["DAL", "AUS", "OKC"],
    "east":       ["ATL", "CLT", "PIT"],
    "west":       ["SEA", "LAX", "SFO"],
    "southeast":  ["MIA", "JAX", "BNA"],
    "southwest":  ["PHX", "ABQ", "ELP"],
    "northeast":  ["NYC", "BOS", "PHL"],
    "northwest":  ["POR", "GEG", "BOI"]
}

REGION_SUBNET_MAP = {
    "central":    "10.10.0.0/16",
    "east":       "10.20.0.0/16",
    "west":       "10.30.0.0/16",
    "southeast":  "10.40.0.0/16",
    "southwest":  "10.50.0.0/16",
    "northeast":  "10.60.0.0/16",
    "northwest":  "10.70.0.0/16"
}

DEVICE_ROLE_CODES = {
    "edge": "ED",
    "core": "CO",
    "agg":  "AG",
    "dist": "DS",
    "rtr":  "RT",
    "sw":   "SW"
}

OBS_STATUS_WEIGHTED = [
    ("active", 0.7),
    ("degraded", 0.2),
    ("down", 0.07),
    ("retired", 0.03)
]

# --- Utilities ---

def weighted_choice(choices):
    values, weights = zip(*choices)
    return random.choices(values, weights=weights, k=1)[0]

def generate_hostname(region: str) -> str:
    site_code = random.choice(REGION_SITE_MAP[region])
    state_code = SITE_STATE_MAP[site_code]
    role_name = random.choice(list(DEVICE_ROLE_CODES.keys()))
    role_code = DEVICE_ROLE_CODES[role_name]
    num = str(random.randint(1, 99)).zfill(2)
    return f"{site_code}{state_code}{role_code}{num}"

def generate_private_ip(region: str) -> str:
    subnet = ipaddress.IPv4Network(REGION_SUBNET_MAP[region])
    return str(random.choice(list(subnet.hosts())))

# --- Deduplication State ---
seen_ips = set()
seen_hostnames = set()

def generate_unique_asset_row():
    while True:
        region = random.choices(list(REGION_WEIGHTS.keys()), weights=REGION_WEIGHTS.values(), k=1)[0]
        hostname = generate_hostname(region)
        ip_address = generate_private_ip(region)

        if hostname in seen_hostnames or ip_address in seen_ips:
            continue

        seen_hostnames.add(hostname)
        seen_ips.add(ip_address)

        fqdn = f"{hostname}.{region}.lightspeed.net"
        status = weighted_choice(OBS_STATUS_WEIGHTED)
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

# --- Data Generation ---
start_time = time.time()

rows = []
for i in range(NUM_ASSETS):
    rows.append(generate_unique_asset_row())
    if (i + 1) % 1000 == 0:
        logging.info(f"{i + 1} assets generated...")

df = pd.DataFrame(rows)

elapsed = time.time() - start_time
logging.info(f"✅ Completed generation of {NUM_ASSETS} assets in {elapsed:.2f} seconds")

df.to_csv("base_asset_dataset.csv", index=False)
logging.info("📁 Saved to base_asset_dataset.csv")