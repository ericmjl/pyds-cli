"""Utility functions for projects."""
from pathlib import Path
from typing import List


def make_wanted_dirs(project_dir: Path, project_name: str) -> List[Path]:
    """Return a list of wanted directories.

    :param project_dir: Directory of the project.
    :param project_name: Name of the project.
    :returns: A list of wanted directories as Path objects.
    """
    wanted_dirs = [
        project_dir / ".devcontainer",
        project_dir / ".github" / "workflows",
        project_dir / ".github",
        project_dir / "docs",
        project_dir / "tests",
        project_dir / project_name,
    ]
    return wanted_dirs
