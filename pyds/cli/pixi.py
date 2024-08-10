"""Pixi surrogate commands."""

from pathlib import Path

import typer

# from ..utils import run
from sh import pixi, rm

app = typer.Typer()


@app.command()
def rebuild():
    """Rebuild the pixi environment.

    This command should be used
    whenever you suspect that your Pixi environment might be broken.
    This may show up in packages cryptically having files not being found.
    """
    # Check that the directory `.pixi/` exists.
    if not Path(".pixi").exists():
        error_msg = (
            "No `.pixi/` directory found, "
            "so it looks like there's nothing to rebuild! "
            "Feel free to run `pixi install --manifest-path pyproject.toml` "
            "to create your environment."
        )
        raise FileNotFoundError(error_msg)
    rm("-rf", ".pixi")
    pixi("install", "--manifest-path", "pyproject.toml")
