"""Tests for conda sub-commands."""
import os

from typer.testing import CliRunner

from pyds.cli import app

runner = CliRunner()


def test_clean():
    """Test for conda clean wrapper."""
    result = runner.invoke(app, ["conda", "clean"])
    assert result.exit_code == 0


def test_rebuild(initialized_project):
    """Execution test for conda rebuild wrapper.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    tmp_path, project_name = initialized_project
    os.chdir(tmp_path / project_name)
    result = runner.invoke(app, ["conda", "rebuild"])
    assert result.exit_code == 0


def test_update(initialized_project):
    """Execution test for conda update wrapper.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    tmp_path, project_name = initialized_project
    os.chdir(tmp_path / project_name)
    result = runner.invoke(app, ["conda", "update"])
    assert result.exit_code == 0
