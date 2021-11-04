from typer import Typer
import subprocess
import yaml
import os

app = Typer()


@app.command()
def update():
    """Update the conda associated with the project."""
    subprocess.run("conda deactivate && mamba env update -f environment.yml".split())


@app.command()
def rebuild():
    """Rebuild the conda environment from scratch."""
    with open("environment.yml", "r+") as f:
        env_config = yaml.load(f)
        project_name = env_config["name"]
    subprocess.run(f"conda env remove -n {project_name}".split())
    subprocess.run(f"mamba env update -f environment.yml".split())
    subprocess.run(f"python -m pip install -e .".split())


if __name__ == "__main__":
    app()
