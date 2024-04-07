"""Project initialization and state management tools."""

import os

import typer
from cookiecutter.main import cookiecutter
from rich.console import Console

from pyds.utils import run
from pyds.utils.paths import SOURCE_DIR
from pyds.utils.project import (
    configure_git,
    create_environment,
    create_jupyter_kernel,
    install_custom_source_package,
    install_precommit_hooks,
)

console = Console()
app = typer.Typer()


@app.command()
def init():
    """Initialize a new Python data science project."""
    template_dir = SOURCE_DIR / "templates" / "project"
    result = cookiecutter(str(template_dir.resolve()))

    os.chdir(result)

    create_environment()
    create_jupyter_kernel()
    install_custom_source_package()
    configure_git()
    install_precommit_hooks()

    print(
        "[green]🎉Your project repo has been created!"
    )



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
    run("pre-commit autoupdate", show_out=True, activate_env=True)
    run("mamba env update -f environment.yml", show_out=True, activate_env=True)


if __name__ == "__main__":
    app()
