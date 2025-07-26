# src/report/generate_inventory_report.py

import os
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

sns.set(style="whitegrid")

def generate_inventory_report(model_path: str, dataset_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # Load model and dataset
    model = joblib.load(model_path)
    df = pd.read_csv(dataset_path)

    # Split features/labels
    X = df.drop(columns=["missing_in_inventory"])
    y_true = df["missing_in_inventory"]

    # Preprocess
    X.fillna("missing", inplace=True)
    X = pd.get_dummies(X)

    if hasattr(model, "feature_names_in_"):
        missing_cols = set(model.feature_names_in_) - set(X.columns)
        for col in missing_cols:
            X[col] = 0
        X = X[model.feature_names_in_]

    # Predict
    y_pred = model.predict(X)

    # Classification report
    report = classification_report(y_true, y_pred, output_dict=True)
    with open(os.path.join(output_dir, "classification_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Present", "Missing"], yticklabels=["Present", "Missing"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Inventory Model - Confusion Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"))
    plt.close()

    # Feature importance
    if hasattr(model, "feature_importances_"):
        importances = pd.Series(model.feature_importances_, index=X.columns)
        top_features = importances.sort_values(ascending=False).head(20)
        plt.figure(figsize=(8, 6))
        top_features.plot(kind="barh")
        plt.xlabel("Feature Importance")
        plt.title("Inventory Model - Top 20 Features")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "feature_importance.png"))
        plt.close()