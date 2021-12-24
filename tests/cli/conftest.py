"""Project-wide fixtures."""
import os
from pathlib import Path
from typing import Tuple
from uuid import uuid4

import pytest
from typer.testing import CliRunner

from pyds.cli import app
from pyds.utils import read_config, run


@pytest.fixture(scope="session", autouse=True)
def initialized_project() -> Tuple[Path, Path]:
    """Initialize a project.

    :yields: A two-tuple of temp dir path and project directory path.
    """
    runner = CliRunner()

    # Run `pyds configure` only if the config file is not found.
    # This prevents local configurations from being overwritten by the test.
    try:
        read_config()
    except FileNotFoundError:
        runner.invoke(
            app, ["configure"], input="GitHub Bot\nbot@github.com\nbot\nbot\nbot"
        )
    project_name = str(uuid4())
    tmp_path = Path("/tmp/pyds-cli")
    project_dir = tmp_path / project_name
    project_dir.mkdir(parents=True)
    os.chdir(project_dir)

    result = runner.invoke(
        app,
        ["project", "initialize"],
        input=".\nblah\nMIT\nY\nY\nY\n",
    )
    assert result.exit_code == 0, result.stderr
    yield tmp_path, project_name
    run(f"conda env remove -n {project_name}")
    run(f"rm -rf {tmp_path}")
