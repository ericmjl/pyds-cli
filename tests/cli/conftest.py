"""Project-wide fixtures."""
from typing import Tuple
import pytest

from uuid import uuid4
from pathlib import Path

import os

from typer.testing import CliRunner
from pyds.cli import app


@pytest.fixture(scope="session")
def initialized_project() -> Tuple(Path, Path):
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
    assert result.exit_code == 0
    return tmp_path, project_name
