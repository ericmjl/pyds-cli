"""Tools to handle package publishing."""
import typer
from ..utils import get_env_bin_dir, run
from pyprojroot import here
from enum import Enum

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
        ...,
        help="The name of the pip server on which to publish the package. Should be configured in your .pypirc.",
        prompt=True,
    ),
):
    """Publish the custom package to a pip-compatible server.

    :param bump: The part of the version number to bump.
    :param to: The name of the pip server on which to publish the package.
        Should be configured in your .pypirc.
        Can be run from anywhere within the project directory.
    """
    run(f"bumpversion {bump} --verbose --dry-run", show_out=True)
    response = typer.confirm("Please double-check: is the version bump done right?")
    if response:
        run(f"bumpversion {bump} --verbose", show_out=True)
        run("rm dist/*")
        run(f"python -m build {here()}")
        run(f"twine upload -r {to} dist/")


@app.command()
def reinstall(
    env_file: str = typer.Option("environment.yml", help="Environment file name.")
):
    """Reinstall the custom package into the conda environment.

    :param env_file: The filename of the conda environment file.
        Defaults to `environment.yml`.
    """
    ENV_BIN_DIR = get_env_bin_dir(env_file)
    run(f"{ENV_BIN_DIR}/python -m pip install -e .")


if __name__ == "__main__":
    app()
