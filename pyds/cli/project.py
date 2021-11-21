"""Project initialization and state management tools."""

from pathlib import Path
from rich import print

import typer
from caseconverter import snakecase, kebabcase
from rich.progress import track
from rich.console import Console

from pyds.utils.project import standard_dirs
from ..utils import CONDA_EXE, read_config, run, write_file

console = Console()

THIS_PATH = Path(__file__).parent
TEMPLATE_DIR = THIS_PATH / "templates"

app = typer.Typer()


@app.command()
def initialize(
    project_name: str = typer.Option(
        ".",
        help="The project name. Will be snake-cased. Defaults to current working directory.",
        prompt=True,
    ),
    project_description: str = typer.Option(
        ..., help="A one-line description of your project.", prompt=True
    ),
    license: str = typer.Option("MIT", help="Your project's license.", prompt=True),
    auto_create_env: bool = typer.Option(
        True, help="Automatically create environment", prompt=True
    ),
    auto_jupyter_kernel: bool = typer.Option(
        True, help="Automatically expose environment kernel to Jupyter", prompt=True
    ),
    auto_pre_commit: bool = typer.Option(
        True, help="Automatically install pre-commit", prompt=True
    ),
):
    """Initialize a new Python data science project.

    :param project_name: Name of the new project to create.
        Becomes the directory name, kebab-cased,
        and custom source name, snake_cased.
    :param project_description: A one-line description of the project.
    :param license: The license to use for your new project. Defaults to "MIT".
    :param auto_create_env: Whether or not to automatically create
        a new conda environment for the project.
        Defaults to True.
    :param auto_jupyter_kernel: Whether or not to automatically expose
        the new Python environment to Jupyter as a Jupyter kernel.
        Defaults to True.
    :param auto_pre_commit: Whether or not to automatically install
        the pre-commit hooks.
        Defaults to True.
    """
    here = Path.cwd()
    project_dir = here / kebabcase(project_name)

    if project_name == ".":
        project_name = here.name
        project_dir = here

    information = dict(
        project_name=project_name,
        project_description=project_description,
        license=license,
    )
    information.update(read_config())

    wanted_dirs = standard_dirs(project_dir, project_name)

    for directory in track(
        wanted_dirs, description="[blue]Creating directory structure..."
    ):
        directory.mkdir(parents=True, exist_ok=True)

    run("git init", cwd=project_dir, show_out=True)
    run("git commit --allow-empty -m 'init'", cwd=project_dir)
    run("git branch -m main", cwd=project_dir)

    templates = list(TEMPLATE_DIR.glob("**/*.j2"))

    for template in track(templates, description="[blue]Creating template files..."):
        destination_file = project_dir / template.relative_to(TEMPLATE_DIR)
        if "src" in destination_file.parts:
            # project_name has to be snake-cased in order for imports to work.
            destination_file = (
                Path(project_dir) / snakecase(project_name) / destination_file.name
            )

        if not destination_file.exists():
            write_file(
                template_file=template,
                information=information,
                destination_file=destination_file.with_suffix(""),
            )

    if auto_create_env:
        msg = (
            "[bold blue]Creating conda environment (this might take a few moments!)..."
        )
        with console.status(msg):
            run(
                f"bash -c 'source activate base && {CONDA_EXE} env update -f environment.yml'",
                cwd=project_dir,
                show_out=True,
            )

    if auto_jupyter_kernel:
        msg = "[bold blue]Enabling Jupyter kernel discovery of your newfangled conda environment..."
        with console.status(msg):
            run(
                f"python -m ipykernel install --user --name {project_name}",
                cwd=project_dir,
                show_out=True,
                activate_env=True,
            )

    msg = (
        "[bold blue]Installing your custom source package into the conda environment..."
    )
    with console.status(msg):
        run("pip install -e .", cwd=project_dir, activate_env=True)

    msg = "[bold blue]Configuring git..."
    with console.status(msg):
        repo_name = f"{information['github_username']}/{project_name}"
        git_ssh_url = f"git@github.com:{repo_name}"
        run(f"git remote add origin {git_ssh_url}", cwd=project_dir, show_out=True)

    msg = "[bold blue]Configuring pre-commit..."
    with console.status(msg):
        if auto_pre_commit:
            run(
                "pre-commit install --install-hooks",
                cwd=project_dir,
                show_out=True,
                activate_env=True,
            )

    run("git add .", cwd=project_dir, show_out=True)
    run("git commit -m 'Initial commit.'", cwd=project_dir, show_out=True)
    run("git add .", cwd=project_dir, show_out=True)
    run("git commit -m 'Initial commit.'", cwd=project_dir, show_out=True)

    print(
        f"[green]🎉Your project {project_name} is created!\n"
        f"[green]⚠️Make sure that you own a repository named {repo_name} on GitHub."
    )


@app.command()
def minitialize(
    project_name: str = typer.Option(
        ".",
        help="The project name. Will be snake-cased. Defaults to current working directory.",
        prompt=True,
    ),
):
    """Generate minimal scratch-like environment for prototyping purposes.

    This initializes `git`, source directory, tests, docs.
    Conda environment is created, package still installed into environment,
    implying setup.cfg and setup.py.

    We omit:
    - config files
    - pre-commit
    - devcontainer
    - .github

    :param project_name: Name of the new project to create.
        Becomes the directory name, kebab-cased,
        and custom source name, snake_cased.
    """


if __name__ == "__main__":
    app()
