"""Utility functions for projects."""
from pathlib import Path
from typing import Dict, List, Tuple

from caseconverter import kebabcase, snakecase
from jinja2 import Environment, PackageLoader, Template
from rich.console import Console
from rich.progress import track

from pyds.utils import run

from ..utils import CONDA_EXE

SOURCE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = SOURCE_DIR / "cli" / "templates"

jinja2_env = Environment(
    loader=PackageLoader("pyds.cli", "templates"),
    extensions=["jinja2_strcase.StrcaseExtension"],
)


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


def standard_dirs(information) -> List[Path]:
    """Return a list of minimal directories in a project.

    :param information: A dictionary of basic information for the project.
    :returns: A minimal list of directories as Path objects.
    """
    project_dir = information["project_dir"]
    project_name = information["project_name"]
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


def initialize_git(information: dict):
    """Initialize a git repository in a project directory.

    :param information: A dictionary of basic information for the project.
    """
    project_dir = information["project_dir"]
    git_dir = Path(".git")
    if not git_dir.exists:
        run("git init", cwd=project_dir, show_out=True)
        run("git commit --allow-empty -m 'init'", cwd=project_dir)
        run("git branch -m main", cwd=project_dir)


def project_name_to_dir(project_name: str) -> Tuple[str, Path]:
    """Convert project namecreate_environment into a project dir.

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


def copy_templates(templates: List[Path], information: Dict):
    """Copy templates into project directory.

    :param templates: List of paths to templates.
    :param information: A dictionary of basic information for the project.
    """
    project_dir = information["project_dir"]
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
    :param information: A dictionary of basic information for the project.
    :param destination_file: Path to where the filled template should be placed.
    """
    template = jinja2_env.get_template(str(template_file.relative_to(TEMPLATE_DIR)))
    text = template.render(**information)
    destination_file.touch()
    with destination_file.open(mode="w+") as f:
        f.write(text)


def standard_templates() -> List[Path]:
    """Return the standard list of templates.

    :returns: A list of Path objects.
    """
    templates = list(TEMPLATE_DIR.glob("**/*.j2"))
    return templates


def minimal_templates() -> List[Path]:
    """Return a minimal list of templates to copy.

    :returns: A list of Path objects.
    """
    templates = standard_templates()
    keep_keywords = [
        "environment.yml.j2",
        "pyproject.toml.j2",
        "setup.cfg.j2",
        "setup.py.j2",
    ]

    templates_minimal = []
    for template in templates:
        for keyword in keep_keywords:
            if keyword in str(template):
                templates_minimal.append(template)
    return templates_minimal


console = Console()


def create_environment(information):
    """Create conda environment

    :param information: A dictionary of basic information for the project.
    """
    msg = "[bold blue]Creating conda environment (this might take a few moments!)..."
    with console.status(msg):
        run(
            f"bash -c 'source activate base && {CONDA_EXE} env update -f environment.yml'",
            cwd=information["project_dir"],
            show_out=True,
        )


def create_jupyter_kernel(information: Dict):
    """Create jupyter kernel.

    :param information: A dictionary of basic information for the project.
    """
    msg = "[bold blue]Enabling Jupyter kernel discovery of your newfangled conda environment..."
    with console.status(msg):
        run(
            f"python -m ipykernel install --user --name {information['project_name']}",
            cwd=information["project_dir"],
            show_out=True,
            activate_env=True,
        )


def install_custom_source_package(information):
    """Instal custom source package.

    :param information: A dictionary of basic information for the project.
    """
    msg = (
        "[bold blue]Installing your custom source package into the conda environment..."
    )
    with console.status(msg):
        run("pip install -e .", cwd=information["project_dir"], activate_env=True)


def configure_git(information):
    """Configure git.

    :param information: A dictionary of basic information for the project.
    """
    msg = "[bold blue]Configuring git..."
    with console.status(msg):
        repo_name = f"{information['github_username']}/{information['project_name']}"
        git_ssh_url = f"git@github.com:{repo_name}"
        run(
            f"git remote add origin {git_ssh_url}",
            cwd=information["project_dir"],
            show_out=True,
        )


def install_precommit_hooks(information):
    """Install pre-commit.

    :param information: A dictionary of basic information for the project.
    """
    msg = "[bold blue]Configuring pre-commit..."
    with console.status(msg):
        run(
            "pre-commit install --install-hooks",
            cwd=information["project_dir"],
            show_out=True,
            activate_env=True,
        )


def initial_commit(information):
    """Make initial commit of all code.

    :param information: A dictionary of basic information for the project.
    """
    run("git add .", cwd=information["project_dir"], show_out=True)
    run(
        "git commit -m 'Initial commit.'",
        cwd=information["project_dir"],
        show_out=True,
    )
    run("git add .", cwd=information["project_dir"], show_out=True)
    run(
        "git commit -m 'Initial commit.'",
        cwd=information["project_dir"],
        show_out=True,
    )
