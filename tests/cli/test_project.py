"""Tests for project creation and management."""
from pyds.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_project_initialize():
    """Test for project initialization."""
    runner.invoke(app, ["project", "initialize"], input="asdf\nasdf\nMIT\nY\nY\nY\n")
