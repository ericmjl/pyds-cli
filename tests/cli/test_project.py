"""Tests for project creation and management."""
from pathlib import Path

from caseconverter.caseconverter import snakecase

from pyds.cli.project import TEMPLATE_DIR
from typer.testing import CliRunner

runner = CliRunner()


def test_project_initialize(initialized_project):
    """Test for project initialization.

    :param initialized_project: conftest.py fixture.
    """
    tmp_path, project_name = initialized_project
    project_dir = tmp_path / project_name

    expected_files = list(TEMPLATE_DIR.glob("*/**/*.j2"))
    for f in expected_files:
        f = f.resolve().relative_to(TEMPLATE_DIR).with_suffix("")
        if "src" in f.parts:
            f_str = str(f)
            f_str = f_str.replace("src", snakecase(project_name))
            f = Path(f_str)
        assert (project_dir / f).exists()