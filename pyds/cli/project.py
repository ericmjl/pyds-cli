"""Project initialization and state management tools."""

from __future__ import annotations

import os
from typing import Optional

import typer
from cookiecutter.main import cookiecutter

app = typer.Typer()

# Canonical template lives in its own repo so it can evolve independently of pyds-cli.
DEFAULT_COOKIECUTTER_PROJECT_TEMPLATE = (
    "https://github.com/ericmjl/cookiecutter-python-project.git"
)


@app.command()
def init(
    template: Optional[str] = typer.Option(
        None,
        "--template",
        "-t",
        help=(
            "Cookiecutter template: Git URL (https or gh:org/repo), or path to a template "
            "directory. Default: upstream cookiecutter-python-project. "
            "Override with PYDS_COOKIECUTTER_PROJECT_TEMPLATE."
        ),
    ),
    skip_hooks: bool = typer.Option(
        False,
        "--skip-hooks",
        help=(
            "Skip Cookiecutter pre/post generation hooks (no pixi install, git, or prompts). "
            "Useful for automation or when you will run setup manually."
        ),
    ),
) -> None:
    """Initialize a new Python data science project from the Cookiecutter template.

    By default this clones and uses
    https://github.com/ericmjl/cookiecutter-python-project (cached by Cookiecutter).
    Set PYDS_COOKIECUTTER_PROJECT_TEMPLATE to a local checkout for offline development.
    """
    template_ref: str = (
        template
        or os.environ.get("PYDS_COOKIECUTTER_PROJECT_TEMPLATE")
        or DEFAULT_COOKIECUTTER_PROJECT_TEMPLATE
    )
    cookiecutter(template_ref, accept_hooks=not skip_hooks)
