"""CLI for interacting with system tools.

Because pyds relies heavily on the presence of anaconda,
we look for environment variables such as:

- `CONDA_EXE`
- `CONDA_PYTHON_EXE`
- `CONDA_PREFIX`
- `anaconda`
"""

import typer

from ..utils import run
from ..utils.paths import PYPIRC_PATH

app = typer.Typer()


@app.command()
def status():
    """Report status for tools that we expect to have installed.

    We check for the presence of:

    1. A `conda` installation.
    2. A `homebrew` installation.
    3. The presence of a .pypirc file.
    """
    check_pypi()
    check_homebrew()
    check_conda()


def check_conda():
    """Check that `conda` is installed."""
    out = run("which conda", log=False)
    if out.returncode == 0:
        print("✅ Conda found! 🎉")
    else:
        print(
            "❌ Conda not found. "
            "Please run `pyds system bootstrap` to install conda on your system."
        )


def check_homebrew():
    """Check that `homebrew` is installed."""
    out = run("which brew", log=False)
    if out.returncode == 0:
        print("✅ Homebrew installed! 🎉")
    else:
        print("❌ Homebrew not installed. Please run `pyds system init`.")


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


def install_conda():
    """Install conda onto a user's system."""
    run(
        "wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh"  # noqa: E501
    )


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
