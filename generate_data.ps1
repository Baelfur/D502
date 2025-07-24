Write-Output "🚀 Starting synthetic data pipeline..."

$steps = @(
    "synth\generate_base_assets.py",
    "synth\inject_presence_noise.py",
    "synth\parse_hostname_features.py"
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