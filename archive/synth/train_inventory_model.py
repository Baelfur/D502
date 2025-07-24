import pandas as pd

import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

import matplotlib.pyplot as plt
import numpy as np

# Load enriched data
df = pd.read_csv("data/labeled_asset_dataset.csv")

# Define features and target
X = df[["region", "status", "vendor", "model", "role"]]
y = df["present_in_inventory"]

# Encode features
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_encoded = encoder.fit_transform(X)

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)

# Output
print("\n--- Inventory Model Report ---")
print(report)

# Save model & encoder
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/inventory_model.pkl")
joblib.dump(encoder, "models/inventory_encoder.pkl")
print("✅ Inventory model and encoder saved.")

# Create reports directory if needed
os.makedirs("reports", exist_ok=True)

# Get feature names
feature_names = encoder.get_feature_names_out(X.columns)
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
top_n = 20

# Plot
plt.figure(figsize=(10, 6))
plt.barh(range(top_n), importances[indices[:top_n]][::-1])
plt.yticks(range(top_n), feature_names[indices[:top_n]][::-1])
plt.xlabel("Feature Importance")
plt.title("Top Feature Importances")
plt.tight_layout()

# Save to reports/
output_name = "feature_importance_inventory.png" if "inventory" in __file__ else "feature_importance_ipam.png"
plt.savefig(f"reports/{output_name}")
print(f"📊 Feature importance saved to reports/{output_name}")