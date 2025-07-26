import os
import shutil
import stat

# Paths to clean
paths_to_clean = [
    "data/raw/base_asset_dataset.csv",
    "data/raw/labeled_asset_dataset.csv",
    "data/sqlite/d502_assets.db",
    "data/sqlite/dev.db",
    "data/sqlite/mlflow_test.db",
    "data/sqlite/conda_test.db",
    "data/processed/inventory_training_set.csv",
    "data/processed/ipam_training_set.csv",
    "models/inventory_model.pkl",
    "models/ipam_model.pkl",
    "reports/inventory_report.json",
    "reports/ipam_report.json",
]

dirs_to_clean = [
    "mlruns",
    "reports",  # ← this will remove inventory/ and ipam/ subfolders with their contents
    "__pycache__",
]

def handle_remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"🗑️ Removed file: {path}")

def remove_dir(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path, onerror=handle_remove_readonly)
            print(f"🧹 Removed directory: {path}")
        except Exception as e:
            print(f"❌ Failed to remove {path}: {e}")

if __name__ == "__main__":
    print("🔄 Cleaning up pipeline artifacts...")

    for file_path in paths_to_clean:
        remove_file(file_path)

    for dir_path in dirs_to_clean:
        remove_dir(dir_path)

    print("✅ Cleanup complete.")