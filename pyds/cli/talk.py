"""CLI for creating new talk repositories."""


import typer
from cookiecutter.main import cookiecutter

from pyds.utils.paths import SOURCE_DIR

app = typer.Typer()


@app.command()
def init():
    """Initialize a new talk repository."""
    template_dir = SOURCE_DIR / "templates" / "talk"
    cookiecutter(str(template_dir.resolve()))


if __name__ == "__main__":
    app()
