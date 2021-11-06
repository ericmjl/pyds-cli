"""Conda surrogate commands."""
from typer import Typer
from ..utils import run, CONDA_EXE

app = Typer()


@app.command()
def clean():
    """Build docs for the project."""
    run(f"{CONDA_EXE} clean --all")


if __name__ == "__main__":
    app()
