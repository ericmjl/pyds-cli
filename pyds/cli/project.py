"""Project initialization and state management tools."""

import typer
from rich import print
from rich.console import Console

from pyds.utils import read_config, run
from pyds.utils.project import (
    configure_git,
    copy_templates,
    create_environment,
    create_jupyter_kernel,
    initialize_git,
    install_custom_source_package,
    install_precommit_hooks,
    make_dirs_if_not_exist,
    minimal_dirs,
    minimal_templates,
    project_name_to_dir,
    standard_dirs,
    standard_templates,
)

console = Console()
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
    project_name, project_dir = project_name_to_dir(project_name)

    information = dict(
        project_name=project_name,
        project_dir=project_dir,
        project_description=project_description,
        license=license,
    )
    information.update(read_config())

    wanted_dirs = standard_dirs(information)
    make_dirs_if_not_exist(wanted_dirs)

    initialize_git(information)

    templates = standard_templates()
    copy_templates(templates, information)

    if auto_create_env:
        create_environment(information)

    if auto_jupyter_kernel:
        create_jupyter_kernel(information)

    install_custom_source_package(information)

    configure_git(information)

    if auto_pre_commit:
        install_precommit_hooks(information)

    repo_name = f"{information['github_username']}/{information['project_name']}"

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
    project_name, project_dir = project_name_to_dir(project_name)
    information = dict(
        project_dir=project_dir,
        project_name=project_name,
    )
    information.update(read_config())

    wanted_dirs = minimal_dirs(project_dir, project_name)
    make_dirs_if_not_exist(wanted_dirs)

    initialize_git(information)

    templates = minimal_templates()
    copy_templates(templates, information)
    create_environment(information)
    create_jupyter_kernel(information)
    install_custom_source_package(information)
    configure_git(information)
    install_precommit_hooks(information)


@app.command()
def update():
    """Update the project.

    This command will automatically update the pre-commit hooks
    as well as the conda environment.

    We run the commands with the base conda environment activated
    rather than the project environment
    to prevent phantom child environments from being created.
    This is a known issue with mamba.
    """
    run("pre-commit autoupdate", show_out=True)
    run("mamba env update -f environment.yml", show_out=True)


if __name__ == "__main__":
    app()
