"""Utility functions for projects."""
from pathlib import Path
from typing import Dict, List, Tuple
from caseconverter import snakecase
from caseconverter.caseconverter import kebabcase
from rich.progress import track
from pyds.utils import run
from jinja2 import Template


SOURCE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = SOURCE_DIR / "cli" / "templates"


def minimal_dirs(project_dir: Path, project_name: str) -> List[Path]:
    """Return a list of minimal directories in a project.

    :param project_dir: Directory of the project.
    :param project_name: Name of the project.
    :returns: A minimal list of directories as Path objects.
    """
    dirs = [
        project_dir / "docs",
        project_dir / "tests",
        project_dir / snakecase(project_name),
    ]
    return dirs


def standard_dirs(project_dir: Path, project_name: str) -> List[Path]:
    """Return a list of minimal directories in a project.

    :param project_dir: Directory of the project.
    :param project_name: Name of the project.
    :returns: A minimal list of directories as Path objects.
    """
    dirs = minimal_dirs(project_dir, project_name)

    additional_dirs = [
        project_dir / ".devcontainer",
        project_dir / ".github",
        project_dir / ".github" / "workflows",
    ]
    dirs.extend(additional_dirs)
    return dirs


def make_dirs_if_not_exist(dirs: List[Path]):
    """Make directories if they do not exist.

    :param dirs: A list of pathlib.Path objects.
    """
    for dir in track(dirs, description="[blue]Creating directory structure..."):
        dir.mkdir(parents=True, exist_ok=True)


def initialize_git(project_dir: Path):
    """Initialize a git repository in a project directory.

    :param project_dir: The path to the project directory.
    """
    run("git init", cwd=project_dir, show_out=True)
    run("git commit --allow-empty -m 'init'", cwd=project_dir)
    run("git branch -m main", cwd=project_dir)


def minstall_templates():
    """Install minimal set of templates."""


def project_name_to_dir(project_name: str) -> Tuple[str, Path]:
    """Convert project name into a project dir.

    The behaviour of this function is as follows:

    1. By default, the project name is as-supplied,
    while the project dir will be kebab-cased.
    2. There is one special case: if "." is supplied as the project name,
    then the name of the current directory is used as the project name,
    while the project_dir is set to the current directory.

    :param project_name: User-supplied project name.
    :returns: A 2-tuple of `(project_name, project_dir)`.
    """
    here = Path.cwd()
    project_dir = here / kebabcase(project_name)

    if project_name == ".":
        project_name = here.name  # get the name of the current dir.
        project_dir = here

    return project_name, project_dir


def copy_templates(templates: List[Path], project_dir: Path, information: Dict):
    """Copy templates into project directory.

    :param templates: List of paths to templates.
    :param project_dir: Path to the project directory.
    :param information: A dictionary of basic information for the project.
    """

    for template in track(templates, description="[blue]Creating template files..."):
        destination_file = project_dir / template.relative_to(TEMPLATE_DIR)
        if "src" in destination_file.parts:
            # project_name has to be snake-cased in order for imports to work.
            destination_file = (
                Path(project_dir)
                / snakecase(information["project_name"])
                / destination_file.name
            )

        if not destination_file.exists():
            write_template(
                template_file=template,
                information=information,
                destination_file=destination_file.with_suffix(""),
            )


def read_template(path: Path) -> Template:
    """Return the jinja2 template.

    :param path: Path to template.
    :returns: A jinja2 Template object.
    """
    with open(path, "r+") as f:
        return Template(f.read())


def write_template(template_file: Path, information: dict, destination_file: Path):
    """Write a template file to disk.

    :param template_file: Path to a template.
    :param information: Dictionary of information to populate in the template.
    :param destination_file: Path to where the filled template should be placed.
    """
    template = read_template(template_file)
    text = template.render(**information)
    destination_file.touch()
    with destination_file.open(mode="w+") as f:
        f.write(text)
