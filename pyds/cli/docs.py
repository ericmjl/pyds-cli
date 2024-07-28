"""Wrapper commands for the important mkdocs commands."""

from sh import pixi
from typer import Typer

app = Typer()


@app.command()
def build():
    """Build docs for the project."""
    pixi("run", "-e", "docs", "docs-build")


@app.command()
def serve():
    """Serve docs for the project."""
    pixi("run", "-e", "docs", "docs-serve")


if __name__ == "__main__":
    app()
