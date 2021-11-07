"""Wrapper commands for the important mkdocs commands."""
from pathlib import Path
import subprocess
from typer import Typer
from ..utils import get_env_bin_dir, run


subprocess

app = Typer()


@app.command()
def build():
    """Build docs for the project."""
    ENV_BIN_DIR = get_env_bin_dir()

    run(f"{ENV_BIN_DIR}/mkdocs build")


@app.command()
def serve():
    """Serve docs for the project."""
    ENV_BIN_DIR = get_env_bin_dir()
    cmd = f"{ENV_BIN_DIR}/mkdocs serve"
    run(cmd, show_out=True)


if __name__ == "__main__":
    app()
