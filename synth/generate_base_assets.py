import random
import pandas as pd
from faker import Faker
import ipaddress
import logging
import time

from shared.constants import (
    ROLE_VENDOR_MODEL_MAP,
    DEVICE_ROLE_CODES,
    REGION_WEIGHTS,
    ROLE_WEIGHTS,
    OBS_STATUS_WEIGHTED,
    REGION_SITE_MAP,
    SITE_STATE_MAP,
    REGION_SUBNET_MAP
)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

# --- Initialization ---
fake = Faker()
NUM_ASSETS = 10_000

# --- Utilities ---

def weighted_choice(choices_dict):
    values, weights = zip(*choices_dict.items())
    return random.choices(values, weights=weights, k=1)[0]

def generate_hostname(region: str, role: str) -> str:
    site_code = random.choice(REGION_SITE_MAP[region])
    state_code = SITE_STATE_MAP[site_code]
    role_code = DEVICE_ROLE_CODES[role]
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
        region = weighted_choice(REGION_WEIGHTS)
        role = weighted_choice(ROLE_WEIGHTS)
        hostname = generate_hostname(region, role)
        ip_address = generate_private_ip(region)

        if hostname in seen_hostnames or ip_address in seen_ips:
            continue

        seen_hostnames.add(hostname)
        seen_ips.add(ip_address)

        fqdn = f"{hostname}.{region}.lightspeed.net"
        status = weighted_choice(dict(OBS_STATUS_WEIGHTED))
        vendor, model = random.choice(ROLE_VENDOR_MODEL_MAP[role])

        return {
            "ip_address": ip_address,
            "hostname": hostname,
            "fqdn": fqdn,
            "region": region,
            "status": status,
            "vendor": vendor,
            "model": model,
            "role": role
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