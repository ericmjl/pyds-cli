"""Tests for project creation and management."""
import os
from pathlib import Path

from pyds.cli import app
from pyds.cli.project import TEMPLATE_DIR
from typer.testing import CliRunner

runner = CliRunner()


def test_project_initialize(tmp_path):
    """Test for project initialization.

    :param tmp_path: Built-in pytest fixture to generate temporary directory.
    """
    os.chdir(tmp_path)
    runner.invoke(app, ["project", "initialize"], input="asdf\nasdf\nMIT\nN\nY\nY\n")

    project_dir = tmp_path / "asdf"

    expected_files = list(TEMPLATE_DIR.glob("*/**/*.j2"))
    for f in expected_files:
        f = f.resolve().relative_to(TEMPLATE_DIR).with_suffix("")
        if "src" in f.parts:
            f_str = str(f)
            f_str = f_str.replace("src", "asdf")
            f = Path(f_str)
        assert (project_dir / f).exists()
