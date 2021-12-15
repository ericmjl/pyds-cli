"""Project-wide fixtures."""
import os
from pathlib import Path
from typing import Tuple
from uuid import uuid4

import pytest
from typer.testing import CliRunner

from pyds.cli import app


@pytest.fixture(scope="session")
def initialized_project() -> Tuple[Path, Path]:
    """Initialize a project.

    :returns: A two-tuple of temp dir path and project directory path.
    """
    runner = CliRunner()
    project_name = str(uuid4())
    tmp_path = Path("/tmp") / str(uuid4())
    project_dir = tmp_path / project_name
    project_dir.mkdir(parents=True)
    os.chdir(project_dir)

    result = runner.invoke(
        app,
        ["project", "initialize"],
        input=".\nblah\nMIT\nY\nY\nY\n",
    )
    assert result.exit_code == 0, result.stderr
    return tmp_path, project_name


@pytest.fixture(scope="session")
def minimal_project() -> Tuple[Path, Path]:
    """Initialize a _minimal_ project.

    :returns: A two-tuple of temp dir path and project directory path.
    """
    runner = CliRunner()
    project_name = str(uuid4())
    tmp_path = Path("/tmp") / str(uuid4())
    project_dir = tmp_path / project_name
    project_dir.mkdir(parents=True)
    os.chdir(project_dir)

    result = runner.invoke(
        app,
        ["project", "minitialize"],
        input=".\n",
    )
    assert result.exit_code == 0
    return tmp_path, project_name
