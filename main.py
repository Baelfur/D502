import argparse
import subprocess
import os
import sys

def run_generate(args):
    cmd = [
        sys.executable,
        "src/generate/main.py",
        "--num_assets", str(args.num_assets),
        "--seed", str(args.seed),
        "--raw_dir", args.raw_dir,
        "--sqlite_path", args.sqlite_path
    ]
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="Run D502 data pipeline")
    subparsers = parser.add_subparsers(dest="stage", required=True)

    # --- Generate ---
    generate_parser = subparsers.add_parser("generate", help="Generate synthetic data")
    generate_parser.add_argument("--num_assets", type=int, default=11246)
    generate_parser.add_argument("--seed", type=int, default=42)
    generate_parser.add_argument("--raw_dir", type=str, default="data/raw")
    generate_parser.add_argument("--sqlite_path", type=str, default="data/sqlite/d502_assets.db")

    args = parser.parse_args()

    if args.stage == "generate":
        run_generate(args)

if __name__ == "__main__":
    main()