import wandb
import logging
from sklearn.metrics import classification_report

logger = logging.getLogger(__name__)

def init_wandb(project_name: str, config: dict):
    """
    Initialize a Weights & Biases run.

    Args:
        project_name (str): The W&B project name
        config (dict): Configuration dictionary to log
    """
    try:
        wandb.init(project=project_name, config=config)
        logger.info("🟢 Weights & Biases initialized.")
    except Exception as e:
        logger.warning(f"⚠️ Could not initialize W&B: {e}")

def log_classification_report(y_true, y_pred):
    """
    Log classification metrics to W&B.

    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
    """
    try:
        report_dict = classification_report(y_true, y_pred, output_dict=True)
        wandb.log(report_dict)
        logger.info("📊 Classification report logged to Weights & Biases.")
    except Exception as e:
        logger.warning(f"⚠️ Failed to log classification report to W&B: {e}")