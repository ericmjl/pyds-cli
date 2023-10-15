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

    Because we assume that the test is always executed from within a conda env,
    it must return exit code 1, rather than 0.
    This is b/c we expect the the `pyds conda update` command to be executed
    from within the _base_ env and not a project-specific env.


    :param initialized_project: conftest.py fixture for our initialized project.
    """
    tmp_path, project_name = initialized_project
    os.chdir(tmp_path / project_name)
    result = runner.invoke(app, ["conda", "rebuild"])
    assert result.exit_code == 1


def test_update(initialized_project):
    """Execution test for conda update wrapper.

    Because we assume that the test is always executed from within a conda env,
    it must return exit code 1, rather than 0.
    This is b/c we expect the the `pyds conda update` command to be executed
    from within the _base_ env and not a project-specific env.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    tmp_path, project_name = initialized_project
    os.chdir(tmp_path / project_name)
    result = runner.invoke(app, ["conda", "update"])
    assert result.exit_code == 1
