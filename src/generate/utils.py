# src/generate/utils.py

import random
from faker import Faker
from synth.shared.constants import (
    SITE_STATE_MAP,
    ROLE_VENDOR_MODEL_MAP
)

fake = Faker()

def generate_unique_asset_row():
    site_code = random.choice(list(SITE_STATE_MAP.keys()))
    state_code = SITE_STATE_MAP[site_code]
    role_code = random.choice(list(ROLE_VENDOR_MODEL_MAP.keys()))

    vendor_model_pairs = ROLE_VENDOR_MODEL_MAP[role_code]
    vendor, model = random.choice(vendor_model_pairs)

    hostname = fake.unique.lexify(text="??????????").lower()
    hostname = f"{site_code}{state_code}{role_code}-{hostname}"

    region = site_code  # Simplified; update if needed
    fqdn = f"{hostname}.{region}.lightspeed.net"

    ip_address = fake.unique.ipv4()
    return {
        "ip_address": ip_address,
        "hostname": hostname,
        "fqdn": fqdn,
        "vendor": vendor,
        "model": model,
        "region": region
    }