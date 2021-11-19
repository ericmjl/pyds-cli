"""Tests for environment variables."""
from typer.testing import CliRunner
from pyds.cli import app


runner = CliRunner()


def test_set_env_var(initialized_project):
    """Execution test for setting environment variables.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    result = runner.invoke(app, ["env", "set-env-var", "key", "value"])
    assert result.exit_code == 0


def test_delete_env_var(initialized_project):
    """Execution test for setting environment variables.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    result = runner.invoke(app, ["env", "delete-env-var", "key", "value"])
    assert result.exit_code == 0


def test_show_env_vars(initialized_project):
    """Execution test for displaying environment variables.

    :param initialized_project: conftest.py fixture for our initialized project.
    """
    result = runner.invoke(app, ["env", "show-env-vars", "key", "value"])
    assert result.exit_code == 0
