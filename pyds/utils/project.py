"""Utility functions for projects."""
from pathlib import Path
from typing import List, Tuple

import yaml
from caseconverter import kebabcase, snakecase
from rich.console import Console

from pyds.utils import run

from ..utils import CONDA_EXE, get_conda_env_name

# jinja2_env = Environment(
#     loader=PackageLoader("pyds.cli", "templates"),
#     extensions=["jinja2_strcase.StrcaseExtension"],
# )


def minimal_dirs(project_dir: Path, project_name: str) -> List[Path]:
    """Return a list of minimal directories in a project.

    :param project_dir: Directory of the project.
    :param project_name: Name of the project.
    :returns: A minimal list of directories as Path objects.
    """
    dirs = [
        project_dir / "docs",
        project_dir / "tests",
        project_dir / snakecase(project_name),
    ]
    return dirs


def standard_dirs(information) -> List[Path]:
    """Return a list of minimal directories in a project.

    :param information: A dictionary of basic information for the project.
    :returns: A minimal list of directories as Path objects.
    """
    project_dir = information["project_dir"]
    project_name = information["project_name"]
    dirs = minimal_dirs(project_dir, project_name)

    additional_dirs = [
        project_dir / ".devcontainer",
        project_dir / ".github",
        project_dir / ".github" / "workflows",
    ]
    dirs.extend(additional_dirs)
    return dirs


def initialize_git(information: dict):
    """Initialize a git repository in a project directory.

    :param information: A dictionary of basic information for the project.
    """
    project_dir = information["project_dir"]
    git_dir = Path(".git")
    if not git_dir.exists:
        run("git init", cwd=project_dir, show_out=True)
        run("git commit --allow-empty -m 'init'", cwd=project_dir)
        run("git branch -m main", cwd=project_dir)


def project_name_to_dir(project_name: str) -> Tuple[str, Path]:
    """Convert project name into a project dir.

    The behaviour of this function is as follows:

    1. By default, the project name is as-supplied,
    while the project dir will be kebab-cased.
    2. There is one special case: if "." is supplied as the project name,
    then the name of the current directory is used as the project name,
    while the project_dir is set to the current directory.

    :param project_name: User-supplied project name.
    :returns: A 2-tuple of `(project_name, project_dir)`.
    """
    here = Path.cwd()
    project_dir = here / kebabcase(project_name)

    if project_name == ".":
        project_name = here.name  # get the name of the current dir.
        project_dir = here

    return project_name, project_dir


console = Console()


def create_environment():
    """Create conda environment

    :param information: A dictionary of basic information for the project.
    """
    msg = "[bold blue]Creating conda environment (this might take a few moments!)..."
    with console.status(msg):
        run(
            f"{CONDA_EXE} env update -f environment.yml",
            show_out=True,
        )


def create_jupyter_kernel():
    """Create jupyter kernel."""
    msg = (
        "[bold blue]Enabling Jupyter kernel discovery "
        "of your newfangled conda environment..."
    )
    # Read environment.yml and get the environment name.
    project_name = get_conda_env_name()
    with console.status(msg):
        run(
            f"python -m ipykernel install --user --name {project_name}",
            show_out=True,
            activate_env=True,
        )


def install_custom_source_package():
    """Instal custom source package."""
    msg = (
        "[bold blue]Installing your custom source package into the conda environment..."
    )
    with console.status(msg):
        run("pip install -e .", activate_env=True)


def configure_git():
    """Configure git.

    :param information: A dictionary of basic information for the project.
    """
    msg = "[bold blue]Configuring git..."

    with open("mkdocs.yaml", "r+") as f:
        mkdocs_config = yaml.safe_load(f)
        repo_url = mkdocs_config["repo_url"]

    *unnecessary, github_username, repo_name = repo_url.split("/")

    run("git init", show_out=True)
    with console.status(msg):
        full_repo_name = f"{github_username}/{repo_name}"
        git_ssh_url = f"git@github.com:{full_repo_name}"
        run(
            f"git remote add origin {git_ssh_url}",
            show_out=True,
        )


def install_precommit_hooks():
    """Install pre-commit.

    :param information: A dictionary of basic information for the project.
    """
    msg = "[bold blue]Configuring pre-commit..."
    with console.status(msg):
        run(
            "pre-commit install --install-hooks",
            show_out=True,
            activate_env=True,
        )


def initial_commit(information):
    """Make initial commit of all code.

    :param information: A dictionary of basic information for the project.
    """
    run("git add .", cwd=information["project_dir"], show_out=True)
    run(
        "git commit -m 'Initial commit.'",
        cwd=information["project_dir"],
        show_out=True,
    )
    run("git add .", cwd=information["project_dir"], show_out=True)
    run(
        "git commit -m 'Initial commit.'",
        cwd=information["project_dir"],
        show_out=True,
    )
