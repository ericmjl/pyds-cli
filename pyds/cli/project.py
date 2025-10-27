"""Project initialization and state management tools."""

import typer
from rich.console import Console

from pyds.utils.paths import SOURCE_DIR

console = Console()
app = typer.Typer()


@app.command()
def init():
    """Initialize a new Python data science project."""
    template_dir = SOURCE_DIR / "templates" / "project"
    cookiecutter(str(template_dir.resolve()))


if __name__ == "__main__":
    app()
