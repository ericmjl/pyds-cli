"""CLI for interacting with system tools.

Because pyds relies heavily on the presence of anaconda,
we look for environment variables such as:

- `CONDA_EXE`
- `CONDA_PYTHON_EXE`
- `CONDA_PREFIX`
- `anaconda`
"""

import typer
from sh import bash, curl, which

from ..utils.paths import PYPIRC_PATH

app = typer.Typer()


@app.command()
def status():
    """Report status for tools that we expect to have installed.

    We check for the presence of:

    1. A `pixi` installation.
    2. A `homebrew` installation.
    3. The presence of a .pypirc file.
    """
    check_pypi()
    check_pixi()


def check_pixi():
    """Check that `pixi` is installed."""
    out = which("pixi")
    if out:
        location = out.strip("\n")
        print(f"✅ pixi found at {location}! 🎉")
    else:
        print(
            "❌ pixi not found. "
            "Please follow instructions at https://pixi.sh/install.sh to install pixi."
        )


def check_pypi():
    """Check that there is a .pypirc configuration file."""
    if PYPIRC_PATH.exists():
        print("✅ ~/.pypirc exists! 🎉")
    else:
        print(
            "❌ ~/.pypirc not found. "
            "Please run `pyds system bootstrap` to create the `.pypirc` file."
        )


@app.command()
def init():
    """Bootstrap user's system with necessary programs."""
    install_pypirc()
    install_pixi()


def install_pixi():
    """Install conda onto a user's system."""
    # curl -fsSL https://pixi.sh/install.sh | bash
    curl("-fsSL", "https://pixi.sh/install.sh", "-o", "/tmp/install_pixi.sh")
    bash("/tmp/install_pixi.sh")


def install_homebrew():
    """Install homebrew onto a user's system."""
    pass


def install_pypirc():
    """Create the .pypirc file."""
    if not PYPIRC_PATH.exists():
        PYPIRC_PATH.touch()

        with PYPIRC_PATH.open("w+") as f:
            f.write(
                """# .pypirc file.
# Read more at: https://packaging.python.org/specifications/pypirc/
[distutils]
index-servers =
    pypi
    testpypi
    private-repository

[pypi]
username = __token__
password = <PyPI token>

# [testpypi]
# username = __token__
# password = <TestPyPI token>

# [private-repository]
# repository = <private-repository URL>
# username = <private-repository username>
# password = <private-repository password>
"""
            )
            PYPIRC_PATH.chmod(600)
            print("✅ ~/.pypirc created! 🎉")
            print("ℹ️ Don't forget to edit the file with your own credentials!")


if __name__ == "__main__":
    app()
