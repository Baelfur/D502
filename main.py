# main.py

import click

from src.generate.run import run as run_generate
from src.prepare.run import run as run_prepare
from src.train.run import run as run_train

@click.command()
@click.option(
    "--steps",
    default="generate,prepare,train",
    type=str,
    help="Comma-separated list of steps to execute. Options: generate, prepare, train"
)
def main(steps):
    steps_to_run = [s.strip() for s in steps.split(",")]

    if "generate" in steps_to_run:
        print("🚀 Running generate step")
        run_generate()

    if "prepare" in steps_to_run:
        print("🚀 Running prepare step")
        run_prepare()

    if "train" in steps_to_run:
        print("🚀 Running train step")
        run_train()

if __name__ == "__main__":
    main()