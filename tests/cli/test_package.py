"""Tests for the pyds package subcommand."""


from typer.testing import CliRunner

from pyds.cli import app

runner = CliRunner()


def test_reinstall(initialized_project):
    """Test reinstall sub-command.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    result = runner.invoke(app, ["package", "reinstall"])
    assert result.exit_code == 0
