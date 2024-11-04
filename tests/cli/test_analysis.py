"""Tests for analysis project creation and management."""

import os

from typer.testing import CliRunner

from pyds.cli import app
from pyds.cli.analysis import DEFAULT_NOTEBOOK

runner = CliRunner()


def test_dotenv_presence(initialized_analysis):
    """Assert that the .env file is present in the initialized project directory.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    assert (tmp_path / project_name / ".env").exists()


def test_default_notebook_presence(initialized_analysis):
    """Assert that the default notebook is created during initialization.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    assert (tmp_path / project_name / DEFAULT_NOTEBOOK).exists()


def test_create_notebook(initialized_analysis):
    """Test creation of a new notebook with custom name."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(app, ["analysis", "create", "test_notebook.ipynb"])
    assert result.exit_code == 0


def test_create_notebook_with_packages(initialized_analysis):
    """Test creation of a notebook with additional packages."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(
        app,
        ["analysis", "create", "test_notebook.ipynb", "-p", "pandas", "-p", "numpy"],
    )
    assert result.exit_code == 0


def test_add_dependencies(initialized_analysis):
    """Test adding dependencies to an existing notebook.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(
        app, ["analysis", "add", "pandas", "numpy", "--notebook", DEFAULT_NOTEBOOK]
    )
    assert result.exit_code == 0


def test_create_duplicate_notebook(initialized_analysis):
    """Test that creating a duplicate notebook raises an error."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    # Create first notebook
    runner.invoke(app, ["analysis", "create", "test_notebook.ipynb"])

    # Try to create duplicate
    result = runner.invoke(app, ["analysis", "create", "test_notebook.ipynb"])
    assert result.exit_code != 0
    assert "already exists" in result.stdout


def test_add_dependencies_nonexistent_notebook(initialized_analysis):
    """Test adding dependencies to a non-existent notebook raises error.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(
        app, ["analysis", "add", "pandas", "--notebook", "nonexistent.ipynb"]
    )
    assert result.exit_code != 0
    assert "No notebook found" in result.stdout


def test_run_nonexistent_notebook(initialized_analysis):
    """Test that running a non-existent notebook raises error."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(app, ["analysis", "run", "--notebook", "nonexistent.ipynb"])
    assert result.exit_code != 0
    assert "No notebook found" in result.stdout


def test_env_in_gitignore(initialized_analysis):
    """Assert that .env is listed in .gitignore.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    gitignore_path = tmp_path / project_name / ".gitignore"
    assert gitignore_path.exists()
    gitignore_content = gitignore_path.read_text()
    assert ".env" in gitignore_content
