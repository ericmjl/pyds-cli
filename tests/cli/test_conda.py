"""Tests for conda sub-commands."""
from typer.testing import CliRunner
from pyds.cli import app
import os


runner = CliRunner()


def test_clean():
    """Test for conda clean wrapper."""
    runner.invoke(app, ["conda", "clean"])


def test_rebuild(initialized_project):
    """Execution test for conda rebuild wrapper.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    tmp_path, project_name = initialized_project
    os.chdir(tmp_path / project_name)
    runner.invoke(app, ["conda", "rebuild"])
