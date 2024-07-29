"""Tests for project creation and management."""

import os

from typer.testing import CliRunner

runner = CliRunner()


def test_dotenv_presence(initialized_project):
    """Assert that the.env file is present in the initialized project directory.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    tmp_path, project_name = initialized_project
    os.chdir(tmp_path / project_name)

    assert (tmp_path / project_name / ".env").exists()
