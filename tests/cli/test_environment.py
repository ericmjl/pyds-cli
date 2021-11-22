"""Tests for environment variables."""
import pytest
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
    result = runner.invoke(app, ["env", "delete-env-var", "key"])
    assert result.exit_code == 0


@pytest.mark.parametrize("keys", [True, False])
@pytest.mark.parametrize("values", [True, False])
def test_show_env_vars(initialized_project, keys: bool, values: bool):
    """Execution test for displaying environment variables.

    :param initialized_project: conftest.py fixture for our initialized project.
    :param keys: Whether or not to show keys.
    :param values: Whether or not to show values.
    """
    cmd = ["env", "show-env-vars"]
    if keys:
        cmd.append("--keys")
    elif not keys:
        cmd.append("--no-keys")

    if values:
        cmd.append("--values")
    elif not values:
        cmd.append("--no-values")

    result = runner.invoke(app, cmd)
    assert result.exit_code == 0
