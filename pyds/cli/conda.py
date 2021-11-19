"""Conda surrogate commands."""
from typer import Typer
import yaml
from ..utils import run, CONDA_EXE

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
    run(
        f"bash -c 'source activate {project_name} && python -m pip install -e .'",
        show_out=True,
    )


@app.command()
def update():
    """Update the conda environment associated with the project."""
    run(f"bash -c 'source activate base && {CONDA_EXE} env update -f environment.yml'")


if __name__ == "__main__":
    app()
