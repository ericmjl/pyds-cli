"""Wrapper commands for the important mkdocs commands."""
from typer import Typer

from ..utils import run

app = Typer()


@app.command()
def build():
    """Build docs for the project."""
    run("mkdocs build", activate_env=True)


@app.command()
def serve():
    """Serve docs for the project."""
    run("mkdocs serve", show_out=True, activate_env=True)


if __name__ == "__main__":
    app()
