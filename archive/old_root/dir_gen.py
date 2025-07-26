import os

EXCLUDE_DIRS = {"__pycache__", "d502", ".git", "models", "venv"}

with open("directory_structure.txt", "w") as f:
    for root, dirs, files in os.walk(".", topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        level = root.replace(".", "").count(os.sep)
        indent = " " * 4 * level
        f.write(f"{indent}{os.path.basename(root)}/\n")
        subindent = " " * 4 * (level + 1)
        for file in files:
            f.write(f"{subindent}{file}\n")