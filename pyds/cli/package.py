"""Tools to handle package publishing."""

from enum import Enum

import typer

# from ..utils import run

app = typer.Typer()


class BumpPart(str, Enum):
    """Enum for bump."""

    major = "major"
    minor = "minor"
    patch = "patch"


if __name__ == "__main__":
    app()
