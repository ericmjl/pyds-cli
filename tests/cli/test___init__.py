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
        input="GitHub Tester\ngithub@tester.com\ngh.tester\ngh.tester\ngh.tester\n",
    )
    assert result.exit_code == 0
    config = read_config()

    assert config["name"] == "GitHub Tester"
    assert config["email"] == "github@tester.com"
    assert config["twitter_username"] == "gh.tester"
    assert config["linkedin_username"] == "gh.tester"
    assert config["github_username"] == "gh.tester"
