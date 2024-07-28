"""Project initialization and state management tools."""

import os
from pathlib import Path

import typer
import yaml
from cookiecutter.main import cookiecutter
from rich.console import Console
from sh import git, ls, pixi, pre_commit

# from pyds.utils import run
from pyds.utils.paths import SOURCE_DIR
from pyds.utils.project import write_dotenv

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

    write_dotenv()
    # Create environment
    msg = "[bold blue]Creating pixi environment (this might take a few moments!)..."
    with console.status(msg):
        pixi("install", "-e", "dev")
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
    pre_commit("install", "--install-hooks")
    # install_precommit_hooks()

    print("[green]🎉Your project repo has been created!")


@app.command()
def update():
    """Update the project.

    This command will automatically update the pre-commit hooks
    as well as the conda environment.

    We run the commands with the base conda environment activated
    rather than the project environment
    to prevent phantom child environments from being created.
    This is a known issue with mamba.
    """
    pre_commit("autoupdate")
    pixi("install", "-e", "dev")


if __name__ == "__main__":
    app()
