#!/bin/bash

echo "🚀 Starting model training runs..."

CONFIG_DIR="configs"

CONFIGS=(
  "inventory_full.json"
  "ipam_full.json"
  "inventory_from_obs.json"
  "ipam_from_obs.json"
)

for cfg in "${CONFIGS[@]}"; do
  echo ""
  echo "🔧 Training from $CONFIG_DIR/$cfg ..."
  python synth/train_model.py --config "$CONFIG_DIR/$cfg"
done

echo ""
echo "✅ All models trained successfully."
