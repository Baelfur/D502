import logging
from src.generate.base_asset import generate_base_assets
from src.generate.inject_noise import inject_noise

def run():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("🚀 Starting generate step...")
    df = generate_base_assets()
    inject_noise(df)
    logging.info("✅ Generate step complete.")