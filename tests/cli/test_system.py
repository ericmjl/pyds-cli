"""Tests for system commands."""
from typer.testing import CliRunner

from pyds.cli import app

runner = CliRunner()


def test_status():
    """Execution test for docs build command."""
    result = runner.invoke(app, ["system", "status"])
    assert result.exit_code == 0
