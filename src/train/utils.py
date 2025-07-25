import json
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

logger = logging.getLogger(__name__)

def load_config(config_path: str) -> dict:
    """
    Load a JSON config file from the given path.

    Args:
        config_path (str): Path to JSON config file

    Returns:
        dict: Parsed configuration dictionary
    """
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"❌ Failed to load config from {config_path}: {e}")
        raise

def get_model(model_type: str, model_params: dict):
    """
    Return an initialized sklearn model instance.

    Args:
        model_type (str): One of 'random_forest', 'logistic_regression', 'decision_tree'
        model_params (dict): Parameters to pass to model constructor

    Returns:
        sklearn.base.BaseEstimator: Instantiated model
    """
    if model_type == "random_forest":
        return RandomForestClassifier(**model_params)
    elif model_type == "logistic_regression":
        return LogisticRegression(**model_params)
    elif model_type == "decision_tree":
        return DecisionTreeClassifier(**model_params)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
