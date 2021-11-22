"""Utility functions for projects."""
from pathlib import Path
from typing import List
from caseconverter import snakecase
from rich.progress import track
from pyds.utils import run


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


def standard_dirs(project_dir: Path, project_name: str) -> List[Path]:
    """Return a list of minimal directories in a project.

    :param project_dir: Directory of the project.
    :param project_name: Name of the project.
    :returns: A minimal list of directories as Path objects.
    """
    dirs = minimal_dirs(project_dir, project_name)

    additional_dirs = [
        project_dir / ".devcontainer",
        project_dir / ".github",
        project_dir / ".github" / "workflows",
    ]
    dirs.extend(additional_dirs)
    return dirs


def make_dirs_if_not_exist(dirs: List[Path]):
    """Make directories if they do not exist.

    :param dirs: A list of pathlib.Path objects.
    """
    for dir in track(dirs, description="[blue]Creating directory structure..."):
        dir.mkdir(parents=True, exist_ok=True)


def initialize_git(project_dir: Path):
    """Initialize a git repository in a project directory.

    :param project_dir: The path to the project directory.
    """
    run("git init", cwd=project_dir, show_out=True)
    run("git commit --allow-empty -m 'init'", cwd=project_dir)
    run("git branch -m main", cwd=project_dir)


def minstall_templates():
    """Install minimal set of templates."""
