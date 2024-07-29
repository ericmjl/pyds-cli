"""Tests for the top-level CLI."""

from typer.testing import CliRunner

from pyds.cli import app
from pyds.utils import read_config

runner = CliRunner()


def test_configure():
    """Test for configuring the pyds CLI."""
    result = runner.invoke(
        app,
        ["configure"],
        input="Eric Ma\nericmajinglong@gmail.com\nericmjl\nericmjl\nericmjl\n",
    )
    assert result.exit_code == 0
    config = read_config()

    assert config["name"] == "Eric Ma"
    assert config["email"] == "ericmajinglong@gmail.com"
    assert config["twitter_username"] == "ericmjl"
    assert config["linkedin_username"] == "ericmjl"
    assert config["github_username"] == "ericmjl"
