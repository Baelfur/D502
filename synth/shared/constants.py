# constants.py

# Role-to-model mapping (no overlaps)
ROLE_VENDOR_MODEL_MAP = {
    "edge": [
        ("Cisco", "ISR4431"),
        ("Juniper", "SRX345"),
        ("RAD", "ETX-2")
    ],
    "core": [
        ("Juniper", "MX204"),
        ("Cisco", "NCS540"),
        ("Nokia", "7750 SR-1")
    ],
    "agg": [
        ("Arista", "7280R"),
        ("ADVA", "FSP3000")
    ],
    "dist": [
        ("ADVA", "FSP150"),
        ("Juniper", "QFX5120")
    ],
    "rtr": [
        ("Arista", "7050X3")
    ],
    "sw": [
        ("Cisco", "Catalyst9300")
    ]
}

# Device role codes for hostname encoding
DEVICE_ROLE_CODES = {
    "edge": "ED",
    "core": "CO",
    "agg":  "AG",
    "dist": "DS",
    "rtr":  "RT",
    "sw":   "SW"
}

# Role assignment probabilities
ROLE_WEIGHTS = {
    "edge": 0.30,
    "dist": 0.25,
    "sw":   0.20,
    "rtr":  0.10,
    "agg":  0.10,
    "core": 0.05
}

# Status distribution
OBS_STATUS_WEIGHTED = [
    ("active", 0.7),
    ("degraded", 0.2),
    ("down", 0.07),
    ("retired", 0.03)
]

# Region assignment weights
REGION_WEIGHTS = {
    "central": 0.1,
    "east": 0.1,
    "west": 0.2,
    "southeast": 0.05,
    "southwest": 0.05,
    "northeast": 0.25,
    "northwest": 0.25
}

# Region to site code map
REGION_SITE_MAP = {
    "central":    ["DAL", "AUS", "OKC"],
    "east":       ["ATL", "CLT", "PIT"],
    "west":       ["SEA", "LAX", "SFO"],
    "southeast":  ["MIA", "JAX", "BNA"],
    "southwest":  ["PHX", "ABQ", "ELP"],
    "northeast":  ["NYC", "BOS", "PHL"],
    "northwest":  ["POR", "GEG", "BOI"]
}

# Site to state map
SITE_STATE_MAP = {
    "DAL": "TX", "AUS": "TX", "OKC": "OK",
    "ATL": "GA", "CLT": "NC", "PIT": "PA",
    "SEA": "WA", "LAX": "CA", "SFO": "CA",
    "MIA": "FL", "JAX": "FL", "BNA": "TN",
    "PHX": "AZ", "ABQ": "NM", "ELP": "TX",
    "NYC": "NY", "BOS": "MA", "PHL": "PA",
    "POR": "OR", "GEG": "WA", "BOI": "ID"
}

# Subnets by region for IPAM logic
REGION_SUBNET_MAP = {
    "central":    "10.10.0.0/16",
    "east":       "10.20.0.0/16",
    "west":       "10.30.0.0/16",
    "southeast":  "10.40.0.0/16",
    "southwest":  "10.50.0.0/16",
    "northeast":  "10.60.0.0/16",
    "northwest":  "10.70.0.0/16"
}

# IPAM presence probability by region
IPAM_REGION_MISSING_PROBS = {
    "northeast": 0.3,
    "northwest": 0.01,
    "central": 0.01,
    "east": 0.02,
    "west": 0.05,
    "southeast": 0.03,
    "southwest": 0.01
}

INVENTORY_MODEL_MISSING_PROBS = {
    # EDGE DEVICES (high failure)
    "ISR4431": 0.50,
    "SRX345":  0.60,
    "ETX-2":   0.40,
    # CORE (low failure)
    "MX204": 0.01,
    "NCS540": 0.05,
    "7750 SR-1": 0.01,
    # AGG
    "7280R": 0.03,
    "FSP3000": 0.10,
    # DIST
    "FSP150": 0.10,
    "QFX5120": 0.05,
    # RTR
    "7050X3": 0.02,
    # SW
    "Catalyst9300": 0.03
}

# Fallback probabilities
DEFAULT_MODEL_FAILURE_PROB = 0.1
DEFAULT_REGION_FAILURE_PROB = 0.1