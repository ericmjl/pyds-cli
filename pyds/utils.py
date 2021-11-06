from pathlib import Path
from jinja2 import Template
import yaml
from loguru import logger
import subprocess
import os


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


def run(cmd: str, cwd=None, shell: bool = True):
    """Convenience function to run a shell command while also logging the command."""
    logger.info(f"+ {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=shell)


def get_conda_env_name(env_file="environment.yml"):
    """Get conda environment name from the environment specification file."""
    try:
        with open(env_file, "r+") as f:
            env = yaml.safe_load(f.read())
        return env["name"]
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find the environment file {env_file}! "
            "Please `cd` into the directory that contains the appropriate file."
        )


def get_env_bin_dir():
    env_name = get_conda_env_name()
    ENV_BIN_DIR = f"{ANACONDA}/envs/{env_name}/bin"
    return ENV_BIN_DIR
