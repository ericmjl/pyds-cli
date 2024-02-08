"""CLI for creating new talk repositories."""


import typer
from cookiecutter.main import cookiecutter

from pyds.utils.paths import SOURCE_DIR

app = typer.Typer()


@app.command()
def init(talk_name: str = typer.Option(..., help="The name of the talk.", prompt=True)):
    """Initialize a new talk repository."""
    template_dir = SOURCE_DIR / "templates" / "talk"
    cookiecutter(str(template_dir.resolve()), extra_context=dict(talk_name=talk_name))


if __name__ == "__main__":
    app()
