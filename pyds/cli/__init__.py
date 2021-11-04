from os import write
import typer
from pathlib import Path
from jinja2 import Template
from pyds.utils import read_template, write_file
from functools import partial

THIS_PATH = Path(__file__).parent
TEMPLATE_DIR = THIS_PATH / "templates"

app = typer.Typer()


@app.command()
def new(
    project_name: str = typer.Option(
        "", help="The project name. Will be snake-cased.", prompt=True
    ),
    project_description: str = typer.Option(
        "", help="A one-line description of your project.", prompt=True
    ),
    license: str = typer.Option("MIT", help="Your project's license.", prompt=True),
    github_username: str = typer.Option("", help="Your GitHub username.", prompt=True),
    twitter_username: str = typer.Option(
        "", help="Your Twitter username.", prompt=True
    ),
    linkedin_username: str = typer.Option(
        "", help="Your LinkedIn vanity name.", prompt=True
    ),
):
    """Initialize a new Python data science project."""

    information = dict(
        project_name=project_name,
        project_description=project_description,
        license=license,
        github_username=github_username,
        twitter_username=twitter_username,
        linkedin_username=linkedin_username,
    )
    here = Path.cwd()

    project_dir = here / project_name
    docs_dir = project_dir / "docs"
    tests_dir = project_dir / "tests"
    source_dir = project_dir / project_name

    for directory in [docs_dir, tests_dir, source_dir]:
        directory.mkdir(parents=True)

    write_file(
        template_file=TEMPLATE_DIR / "mkdocs.yaml.j2",
        information=information,
        destination_file=project_dir / "mkdocs.yml",
    )

    write_file(
        template_file=TEMPLATE_DIR / "setup.py.j2",
        information=information,
        destination_file=project_dir / "setup.py",
    )


@app.command()
def reinstall():
    """Rebuild the custom package."""


if __name__ == "__main__":
    app()
