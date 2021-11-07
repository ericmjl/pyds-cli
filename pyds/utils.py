from pathlib import Path
from jinja2 import Template
import yaml
from loguru import logger
import subprocess
import os
from pyprojroot import here
from rich import print


CONDA_EXE = os.getenv("CONDA_EXE")
ANACONDA = os.getenv("anaconda")
# CONDA_EXE = "conda"


def read_template(path: Path) -> Template:
    """Return the jinja2 template."""
    with open(path, "r+") as f:
        return Template(f.read())


def write_file(template_file: Path, information: dict, destination_file: Path):
    """Write a template file to disk."""
    template = read_template(template_file)
    text = template.render(**information)
    destination_file.touch()
    with destination_file.open(mode="w+") as f:
        f.write(text)


def read_config():
    """Read configuration file."""
    config_path = Path.home() / ".pyds.yaml"
    with config_path.open("r+") as f:
        return yaml.safe_load(f.read())


def run(
    cmd: str,
    cwd=Path("."),
    shell: bool = True,
    capture_output: bool = True,
    log: bool = True,
    show_out: bool = False,
):
    """Convenience function to run a shell command while also logging the command."""
    if log:
        logger.info(f"+ {cmd}")

    if show_out:
        print("Running command while showing output!")
        out = subprocess.run(
            cmd,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
        )
    else:
        out = subprocess.run(
            cmd,
            cwd=cwd,
            shell=shell,
            capture_output=capture_output,
        )
    return out


def get_conda_env_name(env_file="environment.yml", cwd: Path = Path(".")):
    """Get conda environment name from the environment specification file.

    This function can be executed from anywhere _within_ a project directory.

    We search for `environment.yml` by default.
    """
    try:
        with open(here(cwd) / env_file, "r+") as f:
            env = yaml.safe_load(f.read())
        return env["name"]
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find the environment file {env_file}! "
            "Please `cd` into a project's directory."
        )


def get_env_bin_dir(env_file="environment.yml", cwd: Path = Path(".")):
    """Get the environment bin directory."""
    env_name = get_conda_env_name(env_file=env_file, cwd=cwd)
    ENV_BIN_DIR = f"{ANACONDA}/envs/{env_name}/bin"
    return ENV_BIN_DIR
