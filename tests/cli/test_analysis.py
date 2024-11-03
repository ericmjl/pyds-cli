"""Tests for analysis project creation and management."""

import os
from pathlib import Path
from typing import Generator, Tuple

import pytest
from typer.testing import CliRunner

from pyds.cli.analysis import DEFAULT_NOTEBOOK, app

runner = CliRunner()


@pytest.fixture
def initialized_analysis(tmp_path) -> Generator[Tuple[Path, str], None, None]:
    """Create an initialized analysis project for testing.

    :param tmp_path: pytest fixture for temporary directory
    :yields: Tuple of (tmp_path, project_name)
    """
    os.chdir(tmp_path)

    # Create minimal pyproject.toml first
    with open(tmp_path / "pyproject.toml", "w") as f:
        f.write("""
[tool.poetry]
name = "test-project"
version = "0.1.0"
description = "Test project"
authors = ["Test User <test@example.com>"]
        """)

    # Mock user input for cookiecutter
    result = runner.invoke(
        app,
        ["init"],
        input="\n".join(
            [
                "Test Analysis",  # project_name
                "test-analysis",  # __repo_name
                "test_user",  # github_username
                "Test analysis project",  # project_description
            ]
        ),
    )
    assert result.exit_code == 0

    yield tmp_path, "test-analysis"


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


def test_create_notebook():
    """Test creation of a new notebook with custom name."""
    with runner.isolated_filesystem():
        # Create minimal project structure
        Path("pyproject.toml").write_text("""
[tool.poetry]
name = "test-project"
version = "0.1.0"
description = "Test project"
authors = ["Test User <test@example.com>"]
        """)

        result = runner.invoke(app, ["create", "test_notebook.ipynb"])
        assert result.exit_code == 0


def test_create_notebook_with_packages():
    """Test creation of a notebook with additional packages."""
    with runner.isolated_filesystem():
        # Create minimal project structure
        Path("pyproject.toml").write_text("""
[tool.poetry]
name = "test-project"
version = "0.1.0"
description = "Test project"
authors = ["Test User <test@example.com>"]
        """)

        result = runner.invoke(
            app, ["create", "test_notebook.ipynb", "-p", "pandas", "-p", "numpy"]
        )
        assert result.exit_code == 0


def test_add_dependencies(initialized_analysis):
    """Test adding dependencies to an existing notebook.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(
        app, ["add", "pandas", "numpy", "--notebook", DEFAULT_NOTEBOOK]
    )
    assert result.exit_code == 0


def test_create_duplicate_notebook():
    """Test that creating a duplicate notebook raises an error."""
    with runner.isolated_filesystem():
        # Create first notebook
        runner.invoke(app, ["create", "test_notebook.ipynb"])

        # Try to create duplicate
        result = runner.invoke(app, ["create", "test_notebook.ipynb"])
        assert result.exit_code != 0
        assert "already exists" in result.stdout


def test_add_dependencies_nonexistent_notebook(initialized_analysis):
    """Test adding dependencies to a non-existent notebook raises error.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(app, ["add", "pandas", "--notebook", "nonexistent.ipynb"])
    assert result.exit_code != 0
    assert "No notebook found" in result.stdout


def test_run_nonexistent_notebook():
    """Test that running a non-existent notebook raises error."""
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["run", "--notebook", "nonexistent.ipynb"])
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
