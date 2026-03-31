"""Project initialization and state management tools."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import typer
from cookiecutter.main import cookiecutter
from rich.console import Console
from sh import git

from pyds.utils import (
    create_github_repo,
    is_gh_authenticated,
    is_gh_installed,
    read_config,
)

console = Console()
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
    no_github: bool = typer.Option(
        False, "--no-github", help="Skip prompting to create a GitHub repository."
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
    project_path = cookiecutter(template_ref, accept_hooks=not skip_hooks)

    if no_github:
        return

    if not is_gh_installed():
        console.print("[yellow]gh CLI is not installed. Skipping GitHub repo creation.")
        console.print(
            "[blue]Install it from https://cli.github.com to enable GitHub repo creation."
        )
        return

    if not is_gh_authenticated():
        console.print(
            "[yellow]gh CLI is not authenticated. Skipping GitHub repo creation."
        )
        console.print("[blue]Run 'gh auth login' to authenticate.")
        return

    try:
        config = read_config()
        github_username = config.get("github_username", "")
    except FileNotFoundError:
        console.print("[yellow]pyds is not configured. Skipping GitHub repo creation.")
        console.print("[blue]Run 'pyds configure' to set up your GitHub username.")
        return

    if not github_username:
        console.print(
            "[yellow]GitHub username not configured. Skipping GitHub repo creation."
        )
        console.print("[blue]Run 'pyds configure' to set your GitHub username.")
        return

    repo_name = Path(project_path).name
    description = f"{repo_name} - created with pyds-cli"

    should_create = typer.confirm(
        f"Create GitHub repository '{github_username}/{repo_name}' on GitHub?"
    )

    if should_create:
        success, error = create_github_repo(repo_name, description)
        if success:
            console.print(
                f"[green]GitHub repository '{github_username}/{repo_name}' created!"
            )
            full_repo_name = f"{github_username}/{repo_name}"
            git_ssh_url = f"git@github.com:{full_repo_name}"
            os.chdir(project_path)
            git("remote", "add", "origin", git_ssh_url)
            console.print(f"[blue]Git remote 'origin' set to {git_ssh_url}")
        else:
            console.print(f"[red]Failed to create GitHub repository: {error}")
