"""Global commands for
"""
import typer
import yaml
from pathlib import Path
from .project import app as project_app
from .conda import app as conda_app
from .env import app as env_app
from .system import app as system_app
from .docs import app as docs_app
from ..utils import run

app = typer.Typer()
app.add_typer(project_app, name="project")
app.add_typer(conda_app, name="conda")
app.add_typer(env_app, name="env")
app.add_typer(system_app, name="system")
app.add_typer(docs_app, name="docs")


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
    """Initial configuration."""
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
def hello():
    print("Hello there!")


if __name__ == "__main__":
    app()
