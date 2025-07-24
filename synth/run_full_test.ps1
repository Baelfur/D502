Write-Output "🚀 Starting synthetic data pipeline..."

$steps = @(
    "generate_base_assets.py",
    "inject_presence_noise.py",
    "parse_hostname_features.py"
)

foreach ($script in $steps) {
    Write-Output "`n▶️ Running $script ..."
    python $script
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Error running $script. Exiting."
        exit 1
    }
}

Write-Output "`n✅ Synthetic data pipeline complete."

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