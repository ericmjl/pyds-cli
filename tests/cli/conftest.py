"""Project-wide fixtures."""

import os
from pathlib import Path
from typing import Generator, Tuple

import pytest
from sh import rm
from typer.testing import CliRunner
from wonderwords import RandomWord

from pyds.cli import app
from pyds.utils import read_config


@pytest.fixture(scope="session", autouse=True)
def initialized_project() -> Generator[Tuple[Path, Path], None, None]:
    """Initialize a project.

    :yields: A two-tuple of temp dir path and project directory path.
    """
    runner = CliRunner(mix_stderr=False)

    # Run `pyds configure` only if the config file is not found.
    # This prevents local configurations from being overwritten by the test.
    try:
        read_config()
    except FileNotFoundError:
        config_result = runner.invoke(
            app, ["configure"], input="GitHub Bot\nbot@github.com\nbot\nbot\nbot"
        )
        if config_result.exit_code != 0:
            print(f"Configuration failed with stdout: {config_result.stdout}")
            print(f"Configuration failed with stderr: {config_result.stderr}")
            raise RuntimeError("Configuration failed")

    tmp_path = Path("/tmp/pyds-cli")
    tmp_path.mkdir(exist_ok=True, parents=True)
    os.chdir(tmp_path)
    r = RandomWord()
    project_name = r.word()

    # Print current working directory and environment for debugging
    print(f"Current working directory: {os.getcwd()}")
    print(f"PIXI_PROJECT_MANIFEST: {os.environ.get('PIXI_PROJECT_MANIFEST')}")

    result = runner.invoke(
        app,
        ["project", "init"],
        input=f"{project_name}\nTest Project\nericmjl\nEric Ma\ne@ma\n",
        catch_exceptions=False,  # Let exceptions bubble up for better error messages
    )

    # Print detailed information about the command result
    print(f"Exit code: {result.exit_code}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
    if hasattr(result, "exception") and result.exception:
        print(f"Exception: {result.exception}")

    # Check if the command succeeded and print error if it failed
    if result.exit_code != 0:
        raise RuntimeError(
            f"Project initialization failed:\n"
            f"Exit code: {result.exit_code}\n"
            f"Stdout: {result.stdout}\n"
            f"Stderr: {result.stderr}"
        )

    project_dir = tmp_path / project_name

    # Verify directory exists before changing into it
    if not project_dir.exists():
        raise RuntimeError(f"Project directory was not created at {project_dir}")

    os.chdir(project_dir)
    yield tmp_path, project_dir

    rm("-rf", tmp_path)
