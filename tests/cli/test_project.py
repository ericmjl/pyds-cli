"""Tests for project creation and management."""

from typer.testing import CliRunner

from pyds.cli import app

runner = CliRunner()


def test_project_update(initialized_project):
    """Test for project initialization.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    result = runner.invoke(app, ["project", "update"])
    assert result.exit_code == 0
