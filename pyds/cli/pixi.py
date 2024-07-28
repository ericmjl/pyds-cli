"""Pixi surrogate commands."""
from pathlib import Path

import typer

from ..utils import run

app = typer.Typer()



@app.command()
def rebuild():
    """Rebuild the pixi environment."""
    # Check that the directory `.pixi/` exists.
    if not Path(".pixi").exists():
        error_msg = """No `.pixi/` directory found!
You should either navigate to the root of your project and run `pyds pixi rebuild`,
or else directly run `pixi install` in your terminal.
"""
        raise FileNotFoundError(error_msg)
    run("rm -rf .pixi/")
    run("pixi install")
