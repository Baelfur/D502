import os
import json
import logging

import mlflow

from src.train.train_model import train_model

CONFIG_DIR = "configs"
TRAIN_DATA_DIR = "train_data"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run():
    logger.info("🚀 Starting train step...")

    # Look for all config files in the config directory
    config_files = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".json")]

    for config_file in config_files:
        config_path = os.path.join(CONFIG_DIR, config_file)
        with open(config_path, "r") as f:
            config = json.load(f)

        model_name = os.path.splitext(config_file)[0]
        logger.info(f"🔧 Training model from config: {config_file}")

        # Start MLflow run
        with mlflow.start_run(run_name=model_name):
            train_model(config=config, model_name=model_name)

    logger.info("✅ Train step complete.")