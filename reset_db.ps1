# Path setup
$DbPath = "synth\sqlite\d502_assets.db"
$HydrateScript = "hydrate_db.py"
$CleanScript = "clean_and_prepare.py"

Write-Host "---- D502 DB Reset Script ----"

# Step 1: Remove the existing database file
if (Test-Path $DbPath) {
    Remove-Item $DbPath -Force
    Write-Host "Deleted existing database: $DbPath"
} else {
    Write-Host "Database not found. Skipping delete."
}

# Step 2: Re-hydrate the database
Write-Host "Running $HydrateScript..."
python $HydrateScript

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: $HydrateScript failed. Aborting." -ForegroundColor Red
    exit 1
}

# Step 3: Clean and prepare data
Write-Host "Running $CleanScript..."
python $CleanScript

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: $CleanScript failed." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Database reset and prepared successfully." -ForegroundColor Green
