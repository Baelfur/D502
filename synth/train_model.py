import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os
import argparse
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


def train_from_config(config_path: str):
    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Load data
    df = pd.read_csv(config["input_file"])

    # Apply feature selection
    if "drop_features" in config:
        df = df.drop(columns=config["drop_features"])

    # Extract features and target
    X = df[config["features"]]
    y = df[config["target"]]
    target_column = config["target"]

    # Encode features
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_encoded = encoder.fit_transform(X)

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=config.get("test_size", 0.2), random_state=config.get("random_state", 42)
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=config.get("n_estimators", 100),
        class_weight="balanced",
        random_state=config.get("random_state", 42)
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("\n--- Model Report ---")
    print(report)

    # Save outputs
    os.makedirs(os.path.dirname(config["output_model"]), exist_ok=True)
    joblib.dump(model, config["output_model"])
    joblib.dump(encoder, config["output_encoder"])
    print("✅ Model and encoder saved.")

    # Feature importance plot
    feature_names = encoder.get_feature_names_out(X.columns)
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    top_n = config.get("top_n_features", 20)

    plt.figure(figsize=(10, 6))
    plt.barh(range(top_n), importances[indices[:top_n]][::-1], color="#e15759")  # red-style for risk
    plt.yticks(range(top_n), feature_names[indices[:top_n]][::-1])
    plt.xlabel("Feature Importance")
    plt.title(f"Top Predictors of {target_column.replace('_', ' ').title()}")
    plt.tight_layout()
    plt.savefig(config["output_plot"])
    print(f"📊 Feature importance plot saved to {config['output_plot']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to JSON config file")
    args = parser.parse_args()

    train_from_config(args.config)