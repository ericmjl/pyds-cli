from typer import Typer
from ..utils import run


app = Typer()


@app.command()
def build():
    """Build docs for the project."""
    run("mkdocs build")


@app.command()
def serve():
    """Serve docs for the project."""
    run("mkdocs serve")


if __name__ == "__main__":
    app()
