"""Tests for project creation and management."""

import os

from typer.testing import CliRunner

from pyds.cli import app

runner = CliRunner()


def test_dotenv_presence(initialized_project):
    """Assert that the.env file is present in the initialized project directory.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    tmp_path, project_name = initialized_project
    os.chdir(tmp_path / project_name)

    assert (tmp_path / project_name / ".env").exists()


def test_project_update(initialized_project):
    """Test for project initialization.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    result = runner.invoke(app, ["project", "update"])
    assert result.exit_code == 0
