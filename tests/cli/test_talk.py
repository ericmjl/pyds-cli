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
            input="\n".join(
                [
                    "dummy talk",
                    "dummy desc",
                    "ericmjl",
                    "Eric Ma",
                    "affiliation",
                    "e@ma",
                ]
            ),
        )
        assert result.exit_code == 0
