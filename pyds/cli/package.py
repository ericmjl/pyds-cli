"""Tools to handle package publishing."""
from enum import Enum

import typer
from pyprojroot import here

from ..utils import run

app = typer.Typer()


class BumpPart(str, Enum):
    """Enum for bump."""

    major = "major"
    minor = "minor"
    patch = "patch"


@app.command()
def publish(
    bump: BumpPart = typer.Option(
        ..., help="Is this a 'major', 'minor', or 'patch' release?", prompt=True
    ),
    to: str = typer.Option(
        "pypi",
        help="The name of the pip server on which to publish the package. Should be configured in your .pypirc.",
        prompt=True,
    ),
    dry_run: bool = typer.Option(
        True,
        help="Whether this is a dry-run or not.",
        prompt=True,
    ),
):
    """Publish the custom package to a pip-compatible server.

    :param bump: The part of the version number to bump.
    :param to: The name of the pip server on which to publish the package.
        Should be configured in your .pypirc.
        Can be run from anywhere within the project directory.
        Defaults to 'pypi'.
    :param dry_run: Whether you want to do just a dry-run.
    """
    run(f"bumpversion {bump} --verbose --dry-run", show_out=True, activate_env=True)
    if not dry_run:
        response = typer.confirm("Please double-check: is the version bump done right?")
        if response:
            run(f"bumpversion {bump} --verbose", show_out=True, activate_env=True)
            run("rm dist/*")
            run(f"python -m build {here()}", activate_env=True)
            run(f"twine upload -r {to} dist/", activate_env=True)


@app.command()
def reinstall(
    env_file: str = typer.Option("environment.yml", help="Environment file name.")
):
    """Reinstall the custom package into the conda environment.

    :param env_file: The filename of the conda environment file.
        Defaults to `environment.yml`.
    """
    run("python -m pip install -e .", activate_env=True)


if __name__ == "__main__":
    app()
