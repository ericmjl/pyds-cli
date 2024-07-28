"""Project initialization and state management tools."""

import os
from pathlib import Path

import typer
import yaml
from cookiecutter.main import cookiecutter
from rich.console import Console
from sh import git, ls, pixi

# from pyds.utils import run
from pyds.utils.paths import SOURCE_DIR

console = Console()
app = typer.Typer()


@app.command()
def init():
    """Initialize a new Python data science project."""
    template_dir = SOURCE_DIR / "templates" / "project"
    project_path = cookiecutter(str(template_dir.resolve()))

    os.chdir(project_path)

    os.environ["PIXI_PROJECT_MANIFEST"] = "pyproject.toml"

    ls("-lah", ".")

    dotenv_text = """# Environment variables for {{ cookiecutter.project_name }}
# NOTE: This file is _never_ committed into the git repository!
#       It might contain secrets (e.g. API keys) that should never be exposed publicly.
# export ENV_VAR="some_value"
"""
    with open(".env", "w") as f:
        f.write(dotenv_text)

    # Create environment
    msg = "[bold blue]Creating pixi environment (this might take a few moments!)..."
    with console.status(msg):
        pixi("install")
    # Create Jupyter kernel:
    msg = (
        "[bold blue]Enabling Jupyter kernel discovery "
        "of your newfangled conda environment..."
    )
    with console.status(msg):
        pixi(
            "run",
            "python",
            "-m",
            "ipykernel",
            "install",
            "--user",
            "--name",
            Path(project_path).name,
        )

    # Configure Git:
    msg = "[bold blue]Configuring git..."

    with open("mkdocs.yaml", "r+") as f:
        mkdocs_config = yaml.safe_load(f)
        repo_url = mkdocs_config["repo_url"]

    *_, github_username, repo_name = repo_url.split("/")

    git("init")
    with console.status(msg):
        full_repo_name = f"{github_username}/{repo_name}"
        git_ssh_url = f"git@github.com:{full_repo_name}"
        git("remote", "add", "origin", git_ssh_url)

    # Install pre-commit hooks:
    pixi("run", "setup")

    print("[green]🎉Your project repo has been created!")


if __name__ == "__main__":
    app()
