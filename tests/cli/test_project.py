"""Tests for project creation and management."""

from typer.testing import CliRunner

runner = CliRunner()


def test_project_initialize(initialized_project):
    """Test for project initialization.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    pass
