"""Analysis project initialization and state management tools."""

import json
import os
from pathlib import Path
from typing import List, Optional

import tomli
import typer
from cookiecutter.main import cookiecutter
from pyprojroot import here
from rich.console import Console
from sh import git, juv, ls, pixi

from pyds.utils.paths import SOURCE_DIR

console = Console()
app = typer.Typer()

DEFAULT_NOTEBOOK_FILENAME = "analysis.ipynb"


def get_default_packages() -> List[str]:
    """Get default packages from pyproject.toml configuration.

    Reads from the pyproject.toml in the root of the git repository.
    """
    pyproject_path = here() / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        config = tomli.load(f)
    return config.get("tool", {}).get("pyds-cli", {}).get("default_packages", [])


def get_python_version() -> str:
    """Get default Python version from pyproject.toml configuration."""
    pyproject_path = here() / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        config = tomli.load(f)
    return config.get("tool", {}).get("pyds-cli", {}).get("python_version", ">=3.10")


def create_notebook_metadata(packages: List[str], python_version: str) -> str:
    """Create notebook metadata according to PEP 723."""
    deps = [f'    "{pkg}",' for pkg in packages]
    deps_str = "\n".join(deps)

    return f"""# /// script
# requires-python = "{python_version}"
# dependencies = [
{deps_str}
# ]
# ///"""


@app.command()
def create(
    name: str = typer.Argument(..., help="Name of the notebook to create"),
    packages: Optional[List[str]] = typer.Option(
        None, "--package", "-p", help="Additional packages to include"
    ),
):
    """Create a new notebook in the notebooks directory with default dependencies."""
    notebooks_dir = Path("notebooks")
    notebooks_dir.mkdir(exist_ok=True)

    # Ensure .ipynb extension
    if not name.endswith(".ipynb"):
        name = f"{name}.ipynb"

    notebook_path = notebooks_dir / name
    if notebook_path.exists():
        raise typer.BadParameter(f"Notebook {name} already exists")

    # Get default configuration
    default_packages = get_default_packages()
    python_version = get_python_version()

    # Combine default and additional packages
    all_packages = default_packages[:]
    if packages:
        all_packages.extend(packages)

    # Create notebook with juv
    juv("init", "--python", python_version, str(notebook_path))

    # Add dependencies
    juv("add", str(notebook_path), *all_packages)

    console.print(f"[green]Created notebook {name} in notebooks directory")
    console.print(f"[blue]Added {len(all_packages)} default packages")
    console.print(
        f"[blue]Run 'pyds analysis run --notebook notebooks/{name}' to start working"
    )


@app.command()
def init(
    python_version: Optional[str] = typer.Option(
        None, "--python", help="Minimum Python version for the analysis"
    ),
    notebook: Path = typer.Option(
        DEFAULT_NOTEBOOK_FILENAME, help="Name of the notebook to create"
    ),
):
    """Initialize a new data analysis project with a juv-managed notebook."""
    # Create project structure from template
    template_dir = SOURCE_DIR / "templates" / "analysis"

    # Get cookiecutter context before running to access variables later
    cookiecutter_json = template_dir / "cookiecutter.json"
    with open(cookiecutter_json) as f:
        context = json.load(f)

    project_path: str = cookiecutter(str(template_dir.resolve()))

    os.chdir(project_path)

    # Ensure notebooks directory exists
    notebooks_dir = Path("notebooks")
    notebooks_dir.mkdir(exist_ok=True)

    # Create initial notebook with juv
    if python_version:
        juv("init", "--python", python_version, str(notebooks_dir / notebook))
    else:
        juv("init", str(notebooks_dir / notebook))

    # Add default packages
    default_packages = get_default_packages()
    if default_packages:
        juv("add", str(notebooks_dir / notebook), *default_packages)

    ls("-lah", ".")

    # Create .env file with template content
    dotenv_path = Path(".env")
    dotenv_template = f"""# Environment variables for {context['project_name']}
# NOTE: This file is _never_ committed into the git repository!
#       It might contain secrets (e.g. API keys) that should never be exposed publicly.

# Add your environment variables here:
# export API_KEY="your_api_key"
# export DATABASE_URL="your_database_url"
"""
    dotenv_path.write_text(dotenv_template)

    # Add .env to .gitignore if not already present
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        gitignore_path.write_text(".env\n")
    else:
        gitignore_content = gitignore_path.read_text()
        if ".env" not in gitignore_content:
            with gitignore_path.open("a") as f:
                f.write("\n.env\n")

    # Create pixi environment for project-level dependencies
    msg = "[bold blue]Creating pixi environment (this might take a few moments!)..."
    with console.status(msg):
        pixi("install")

    # Configure Git
    msg = "[bold blue]Configuring git..."
    git("init", "-b", "main")
    with console.status(msg):
        # Get the github_username from the cookiecutter context
        github_username = context["github_username"]
        repo_name = context["__repo_name"]
        full_repo_name = f"{github_username}/{repo_name}"
        git_ssh_url = f"git@github.com:{full_repo_name}"
        git("remote", "add", "origin", git_ssh_url)

    console.print("[green]🎉Your analysis project has been created!")
    console.print(
        "[blue]Run 'pyds analysis add <package>' to add dependencies to your notebook"
    )
    console.print("[blue]Run 'pyds analysis run' to start working on your analysis")

    git("add", ".")
    git("commit", "-m", "Initial commit")


@app.command()
def add(
    packages: Optional[List[str]] = typer.Option(
        None, "--package", "-p", help="Packages to add to the notebook"
    ),
    notebook: Path = typer.Option(
        DEFAULT_NOTEBOOK_FILENAME, help="Path to the notebook to modify"
    ),
    requirements: Optional[Path] = typer.Option(
        None, "--requirements", help="Requirements file to add dependencies from"
    ),
    extra: Optional[str] = typer.Option(
        None, "--extra", help="Extra dependency group to add (e.g. 'dev')"
    ),
):
    """Add dependencies to the analysis notebook."""
    # Debug prints
    console.print(f"[blue]Packages: {packages}")
    console.print(f"[blue]Notebook: {notebook}")
    console.print(f"[blue]Requirements: {requirements}")
    console.print(f"[blue]Extra: {extra}")
    if not packages and not requirements:
        msg = "Must specify either packages with -p/--package or a requirements file"
        console.print(f"[red]{msg}")
        raise typer.BadParameter(msg)

    notebooks_dir = Path("notebooks")
    notebook_path = notebooks_dir / notebook

    if not notebook_path.exists():
        msg = f"No notebook found at {notebook_path}. Run 'pyds analysis init' first."
        console.print(f"[red]{msg}")
        raise typer.BadParameter(msg)

    # Build the juv command
    cmd = ["add", str(notebook_path)]
    if extra:
        cmd.extend(["--extra", extra])
    if requirements:
        cmd.extend(["--requirements", str(requirements)])
    if packages:
        # Add each package as a separate argument
        cmd.extend(packages)

    # Debug print
    console.print(f"[blue]Running command: juv {' '.join(cmd)}")

    try:
        juv(*cmd)
    except Exception as e:
        msg = f"Error adding dependencies: {str(e)}"
        console.print(f"[red]{msg}")
        raise typer.Exit(1)


@app.command()
def run(
    notebook: Path = typer.Option(
        DEFAULT_NOTEBOOK_FILENAME, help="Path to the notebook to run"
    ),
    jupyter: Optional[str] = typer.Option(
        None, "--jupyter", help="Specific Jupyter frontend to use (e.g. lab, notebook)"
    ),
    extra_deps: Optional[List[str]] = typer.Option(
        None, "--with", help="Additional dependencies for this session"
    ),
):
    """Start working on the analysis in Jupyter."""
    if not notebook.exists():
        raise typer.BadParameter(
            f"No notebook found at {notebook}. "
            "Please provide the path to the notebook "
            "relative to your current working directory in the shell."
        )

    cmd = ["run"]
    if jupyter:
        cmd.extend(["--jupyter", jupyter])
    if extra_deps:
        for dep in extra_deps:
            cmd.extend(["--with", dep])
    cmd.append(str(notebook))

    juv(*cmd)


if __name__ == "__main__":
    app()
