"""Global commands for pyds."""

from pathlib import Path

import typer
import yaml

from pyds.version import __version__

from .environment import app as env_app
from .pixi import app as pixi_app
from .project import app as project_app
from .system import app as system_app
from .talk import app as talk_app

app = typer.Typer()
app.add_typer(env_app, name="env")
app.add_typer(project_app, name="project")
app.add_typer(system_app, name="system")
app.add_typer(talk_app, name="talk")
app.add_typer(pixi_app, name="pixi")


@app.command()
def configure(
    name: str = typer.Option(..., help="Your name", prompt=True),
    email: str = typer.Option(..., help="Your email address", prompt=True),
    github_username: str = typer.Option("", help="Your GitHub username", prompt=True),
    twitter_username: str = typer.Option("", help="Your Twitter username", prompt=True),
    linkedin_username: str = typer.Option(
        "", help="Your LinkedIn username", prompt=True
    ),
):
    """Initial configuration for pyds.

    :param name: Your name.
    :param email: Your email address.
    :param github_username: Your GitHub username.
    :param twitter_username: Your Twitter username.
    :param linkedin_username: Your LinkedIn username.
    """
    info = dict(
        name=name,
        email=email,
        github_username=github_username,
        twitter_username=twitter_username,
        linkedin_username=linkedin_username,
    )
    config_file_path = Path.home() / ".pyds.yaml"
    with config_file_path.open("w+") as f:
        f.write(yaml.dump(info))


@app.command()
def version():
    """Print the current version of pyds."""
    print(__version__)


if __name__ == "__main__":
    app()
