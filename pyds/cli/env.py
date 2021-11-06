from typer import Typer
import yaml
from ..utils import run, CONDA_EXE

app = Typer()


@app.command()
def rebuild():
    """Rebuild the conda environment from scratch."""
    with open("environment.yml", "r+") as f:
        env_config = yaml.load(f)
        project_name = env_config["name"]
    run(f"{CONDA_EXE} env remove -n {project_name}")
    run(f"{CONDA_EXE} env update -f environment.yml")
    run(f"bash -c 'conda activate {project_name}' && python -m pip install -e .")


if __name__ == "__main__":
    app()
