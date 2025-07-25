import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mlflow
import wandb

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from joblib import dump

from src.train.wandb_logging import init_wandb

def train_model(config, model_name):
    input_file = config["input_file"]
    label_column = config["label_column"]
    categorical_features = config["categorical_features"]
    numeric_features = config["numeric_features"]

    df = pd.read_csv(os.path.join("train_data", input_file))
    X = df[categorical_features + numeric_features]
    y = df[label_column]

    X_train, X_val, y_train, y_val = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    # Define transformers
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="mean"))
    ])
    preprocessor = ColumnTransformer([
        ("cat", cat_pipeline, categorical_features),
        ("num", num_pipeline, numeric_features)
    ])

    # Define pipeline
    clf = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42))
    ])

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)

    # Metrics
    report = classification_report(y_val, y_pred, output_dict=True)
    mlflow.log_metrics({
        "precision_1": report["1"]["precision"],
        "recall_1": report["1"]["recall"],
        "f1_1": report["1"]["f1-score"],
        "accuracy": report["accuracy"]
    })

    # Save model
    model_path = os.path.join("artifacts", f"{model_name}_model.joblib")
    os.makedirs("artifacts", exist_ok=True)
    dump(clf, model_path)
    mlflow.log_artifact(model_path)

    # Feature importance
    model = clf.named_steps["classifier"]
    feature_names = clf.named_steps["preprocessor"].get_feature_names_out()
    importances = model.feature_importances_

    # Plot
    top_n = 15
    indices = np.argsort(importances)[::-1][:top_n]
    plt.figure(figsize=(10, 6))
    plt.barh(range(top_n), importances[indices][::-1])
    plt.yticks(range(top_n), [feature_names[i] for i in indices][::-1])
    plt.xlabel("Importance")
    plt.title(f"Top {top_n} Feature Importances: {model_name}")
    plt.tight_layout()
    fig_path = os.path.join("reports", f"feature_importance_{model_name}.png")
    os.makedirs("reports", exist_ok=True)
    plt.savefig(fig_path)
    mlflow.log_artifact(fig_path)

    # W&B logging
    run = init_wandb(model_name=model_name, config=config)
    run.log({
        "model_artifact": wandb.Artifact(f"{model_name}_model", type="model", description="Trained model").add_file(model_path),
        "feature_importance_plot": wandb.Image(fig_path),
        **report["1"]
    })
    run.finish()