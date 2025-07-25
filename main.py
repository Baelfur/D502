import click
from src.generate.run import run as run_generate

@click.command()
@click.option(
    "--steps",
    default="generate",
    type=str,
    help="Comma-separated list of steps to execute. Options: generate,prepare,train"
)
def main(steps):
    steps_to_run = [s.strip() for s in steps.split(",")]

    if "generate" in steps_to_run:
        print("🚀 Running generate step")
        run_generate()

if __name__ == "__main__":
    main()