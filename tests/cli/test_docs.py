"""Tests for docs."""
import os

from typer.testing import CliRunner

from pyds.cli import app

runner = CliRunner()


def test_build(initialized_project):
    """Execution test for docs build command.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    tmp_path, project_name = initialized_project
    project_dir = tmp_path / project_name
    os.chdir(project_dir.resolve())

    result = runner.invoke(app, ["docs", "build"])
    assert result.exit_code == 0
