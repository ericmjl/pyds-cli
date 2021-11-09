"""Global commands for pyds."""
import typer
import yaml
from pathlib import Path
from .initialize import app as initialize_app
from .conda import app as conda_app
from .env import app as env_app
from .system import app as system_app
from .docs import app as docs_app
from .reinstall import app as reinstall_app

app = typer.Typer()
app.add_typer(conda_app, name="conda")
app.add_typer(docs_app, name="docs")
app.add_typer(env_app, name="env")
app.add_typer(initialize_app, name="project")
app.add_typer(reinstall_app, name="reinstall")
app.add_typer(system_app, name="system")


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
    """Initial configuration.

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
def test():
    """Run all tests in the project."""
    print("Hello there!")


if __name__ == "__main__":
    app()
