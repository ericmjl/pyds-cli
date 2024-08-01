"""Project-wide fixtures."""

import os
from pathlib import Path
from typing import Tuple

import pytest
from sh import rm
from typer.testing import CliRunner
from wonderwords import RandomWord

from pyds.cli import app
from pyds.utils import read_config


@pytest.fixture(scope="session", autouse=True)
def initialized_project() -> Tuple[Path, Path]:
    """Initialize a project.

    :yields: A two-tuple of temp dir path and project directory path.
    """
    runner = CliRunner(mix_stderr=False)

    # Run `pyds configure` only if the config file is not found.
    # This prevents local configurations from being overwritten by the test.
    try:
        read_config()
    except FileNotFoundError:
        runner.invoke(
            app, ["configure"], input="GitHub Bot\nbot@github.com\nbot\nbot\nbot"
        )
    tmp_path = Path("/tmp/pyds-cli")
    tmp_path.mkdir(exist_ok=True, parents=True)
    os.chdir(tmp_path)
    r = RandomWord()
    project_name = r.word()

    os.environ["PIXI_PROJECT_MANIFEST"] = ""
    result = runner.invoke(
        app,
        ["project", "init"],
        input=f"{project_name}\nTest Project\nericmjl\nEric Ma\ne@ma\n",
    )
    project_dir = tmp_path / project_name
    os.chdir(project_dir)

    assert result.exit_code == 0, result.stderr
    yield tmp_path, project_name

    rm("-rf", tmp_path)
