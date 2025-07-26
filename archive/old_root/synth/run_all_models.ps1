Write-Output "🚀 Starting model training runs..."

$configs = @(
  "configs/inventory_full.json",
  "configs/ipam_full.json",
  "configs/inventory_from_obs.json",
  "configs/ipam_from_obs.json"
)

foreach ($config in $configs) {
  Write-Output "`n🔧 Training from $config ..."
  python train_model.py --config $config
}

Write-Output "`n✅ All models trained successfully."