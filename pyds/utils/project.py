"""Utility functions for projects."""
from pathlib import Path
from typing import List
from caseconverter import snakecase


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
        project_dir / ".github" / "workflows",
    ]
    dirs.extend(additional_dirs)
    return dirs
