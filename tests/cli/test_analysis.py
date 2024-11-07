"""Tests for analysis project creation and management."""

import os
import traceback
from pathlib import Path
from typing import Generator, Tuple

import pytest
from click.testing import Result
from typer.testing import CliRunner

from pyds.cli import app
from pyds.cli.analysis import DEFAULT_NOTEBOOK_FILENAME
from pyds.cli.analysis import app as analysis_app

# Initialize runner with separate stderr capture
runner = CliRunner(mix_stderr=False)


@pytest.fixture
def initialized_analysis(tmp_path) -> Generator[Tuple[Path, str], None, None]:
    """Create an initialized analysis project for testing.

    :param tmp_path: pytest fixture for temporary directory
    :yields: Tuple of (tmp_path, project_name)
    """
    os.chdir(tmp_path)

    # Mock user input for cookiecutter
    result = runner.invoke(
        app,
        ["analysis", "init"],
        input="\n".join(
            [
                "Test Analysis",  # project_name
                "test-analysis",  # short_description
                "test_user",  # github_username
                "Test analysis project",  # full_name
                "blah@blah.com",  # email
            ]
        ),
        catch_exceptions=False,  # Let exceptions bubble up
    )

    # Print full error details if command fails
    if result.exit_code != 0:
        print("\n=== Command Output ===")
        print(f"Exit code: {result.exit_code}")
        print("\n=== STDOUT ===")
        print(result.stdout or "No stdout")
        print("\n=== STDERR ===")
        print(result.stderr or "No stderr")
        if hasattr(result, "exception"):
            print("\n=== EXCEPTION ===")
            print(f"Exception type: {type(result.exception)}")
            print(f"Exception message: {str(result.exception)}")
            print("\n=== TRACEBACK ===")
            if hasattr(result.exception, "__traceback__"):
                print("".join(traceback.format_tb(result.exception.__traceback__)))

            # For sh.ErrorReturnCode exceptions
            if hasattr(result.exception, "stderr"):
                print("\n=== COMMAND STDERR (full) ===")
                try:
                    print(result.exception.stderr.decode())
                except AttributeError:
                    print(result.exception.stderr)
            if hasattr(result.exception, "stdout"):
                print("\n=== COMMAND STDOUT (full) ===")
                try:
                    print(result.exception.stdout.decode())
                except AttributeError:
                    print(result.exception.stdout)
            if hasattr(result.exception, "full_cmd"):
                print("\n=== FULL COMMAND ===")
                print(result.exception.full_cmd)

    assert result.exit_code == 0, (
        f"Failed to initialize analysis project. Exit code: {result.exit_code}. "
        "See output above."
    )

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

    assert (tmp_path / project_name / "notebooks" / DEFAULT_NOTEBOOK_FILENAME).exists()


def test_create_notebook(initialized_analysis):
    """Test creation of a new notebook with custom name."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(analysis_app, ["create", "test_notebook.ipynb"])
    assert result.exit_code == 0

    assert (tmp_path / project_name / "notebooks" / "test_notebook.ipynb").exists()


def test_create_notebook_with_packages(initialized_analysis):
    """Test creation of a notebook with additional packages."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    # Create notebook with packages
    result: Result = runner.invoke(
        analysis_app,
        ["create", "test_notebook.ipynb", "-p", "pandas", "-p", "numpy"],
    )
    assert result.exit_code == 0, result.stdout

    # Verify notebook exists
    assert (tmp_path / project_name / "notebooks" / "test_notebook.ipynb").exists()


def test_add_dependencies(initialized_analysis):
    """Test adding dependencies to an existing notebook.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(
        analysis_app,
        [
            "add",
            "-p",
            "pandas",
            "-p",
            "numpy",
            "--notebook",
            DEFAULT_NOTEBOOK_FILENAME,
        ],
    )
    # Add debug information
    print("\nCommand output:")
    print(f"Exit code: {result.exit_code}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
    if hasattr(result, "exception"):
        print(f"Exception: {result.exception}")

    assert result.exit_code == 0


def test_add_dependencies_no_packages(initialized_analysis):
    """Test that adding dependencies without specifying packages raises error."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(analysis_app, ["add"])
    assert result.exit_code != 0
    assert "Must specify either packages" in result.stdout


def test_add_dependencies_nonexistent_notebook(initialized_analysis):
    """Test adding dependencies to a non-existent notebook raises error.

    :param initialized_analysis: fixture for initialized analysis project
    """
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(
        analysis_app, ["add", "-p", "pandas", "--notebook", "nonexistent.ipynb"]
    )
    assert result.exit_code != 0
    assert "No notebook found" in result.stderr


def test_create_duplicate_notebook(initialized_analysis):
    """Test that creating a duplicate notebook raises an error."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    # Create first notebook
    first_result = runner.invoke(analysis_app, ["create", "test_notebook.ipynb"])
    assert first_result.exit_code == 0

    # Try to create duplicate
    second_result = runner.invoke(analysis_app, ["create", "test_notebook.ipynb"])
    assert second_result.exit_code != 0
    assert "already exists" in second_result.stdout


def test_run_nonexistent_notebook(initialized_analysis):
    """Test that running a non-existent notebook raises error."""
    tmp_path, project_name = initialized_analysis
    os.chdir(tmp_path / project_name)

    result = runner.invoke(analysis_app, ["run", "--notebook", "nonexistent.ipynb"])
    assert result.exit_code != 0
    assert "No notebook found" in result.stderr


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
