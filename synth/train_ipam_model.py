import pandas as pd

import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load enriched data
df = pd.read_csv("data/labeled_asset_dataset_enriched.csv")

# Define features and target
X = df[["region", "status", "vendor", "model", "role"]]
y = df["present_in_ipam"]

# Encode features
encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
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
print("\n--- IPAM Model Report ---")
print(report)

# Save model & encoder
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/ipam_model.pkl")
joblib.dump(encoder, "models/ipam_encoder.pkl")
print("✅ IPAM model and encoder saved.")
