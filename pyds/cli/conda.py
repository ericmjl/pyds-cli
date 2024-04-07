"""Conda surrogate commands."""
import os

import yaml
from typer import Typer

from ..utils import CONDA_EXE, run

app = Typer()


def ensure_base_env():
    """Ensure that the user is in the base conda environment.

    :raises EnvironmentError: If the user is not in the base conda environment.
    """
    conda_env = os.environ.get("CONDA_DEFAULT_ENV")

    if conda_env != "base":
        raise EnvironmentError(
            "Please run `conda activate base` before running `pyds conda rebuild`!"
        )


@app.command()
def clean():
    """Clean out your conda environment."""
    run("conda clean --all -y")


@app.command()
def rebuild():
    """Rebuild the conda environment from scratch."""
    ensure_base_env()
    with open("environment.yml", "r+") as f:
        env_config = yaml.safe_load(f)
        project_name = env_config["name"]
    run(f"conda env remove -n {project_name}", show_out=True)
    run(f"{CONDA_EXE} env update -f environment.yml", show_out=True)
    run("python -m pip install -e .", show_out=True, activate_env=True)


@app.command()
def update():
    """Update the conda environment associated with the project."""
    ensure_base_env()
    run(f"{CONDA_EXE} env update -f environment.yml")


if __name__ == "__main__":
    app()
