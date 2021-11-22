"""Conda surrogate commands."""
import yaml
from typer import Typer

from ..utils import CONDA_EXE, run

app = Typer()


@app.command()
def clean():
    """Clean out your conda environment."""
    run("conda clean --all -y")


@app.command()
def rebuild():
    """Rebuild the conda environment from scratch."""
    with open("environment.yml", "r+") as f:
        env_config = yaml.safe_load(f)
        project_name = env_config["name"]
    run(f"bash -c 'conda env remove -n {project_name}'", show_out=True)
    run(
        f"bash -c 'source activate base && {CONDA_EXE} env update -f environment.yml'",
        show_out=True,
    )
    run("python -m pip install -e .", show_out=True, activate_env=True)


@app.command()
def update():
    """Update the conda environment associated with the project."""
    run(f"bash -c 'source activate base && {CONDA_EXE} env update -f environment.yml'")


if __name__ == "__main__":
    app()
