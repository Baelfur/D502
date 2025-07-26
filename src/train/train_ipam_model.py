# src/train/train_ipam_model.py

import pandas as pd
import os
import logging
import mlflow
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def train_ipam_model(input_dir: str):
    input_path = os.path.join(input_dir, "ipam_training_set.csv")
    df = pd.read_csv(input_path)

    logging.info(f"📦 Loaded IPAM dataset: {input_path}")
    logging.info(f"🧮 Dataset shape: {df.shape}")

    # Features and label
    X = df.drop(columns=["missing_in_ipam"])
    y = df["missing_in_ipam"]

    # Basic preprocessing
    X.fillna("missing", inplace=True)
    X = pd.get_dummies(X)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

    # Train
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds, output_dict=True)

    logging.info(f"✅ Accuracy: {acc:.4f}")

    # Save model locally to models/
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "ipam_model.pkl")
    joblib.dump(model, model_path)
    logging.info(f"💾 Model saved to: {model_path}")

    # Log to MLflow
    with mlflow.start_run(run_name="ipam_model"):
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")
        mlflow.log_artifact(input_path)
        mlflow.log_dict(report, "classification_report.json")

    logging.info("📦 IPAM model training complete.")