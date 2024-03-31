"""Tests for talk slides creation."""
import os
import tempfile

from typer.testing import CliRunner

from pyds.cli import app

runner = CliRunner()


def test_talk_init():
    """Test for talk initialization."""
    # Run the following command within a temp dir.
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change the current working directory to the temporary directory.
        os.chdir(temp_dir)

        result = runner.invoke(
            app,
            ["talk", "init"],
            input="dummy talk\ndummy desc\nericmjl\nEric Ma\naffiliation\ne@ma\n",
        )
        assert result.exit_code == 0
