"""Tools to handle package publishing."""
import typer
from ..utils import run
from pyprojroot import here
from enum import Enum

app = typer.Typer()


class BumpPart(str, Enum):
    """Enum for bump."""

    major = "major"
    minor = "minor"
    patch = "patch"


@app.command()
def package(
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


def streamlit():
    """Placeholder for possible streamlit publish command."""
    pass


def heroku():
    """Placeholder for possible heroku publish command."""
    pass


def fly():
    """Placeholder for possible future fly publish command."""
    pass


if __name__ == "__main__":
    app()
