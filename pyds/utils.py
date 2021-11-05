from pathlib import Path
from jinja2 import Template
import yaml
from loguru import logger
import subprocess
import os


# CONDA_EXE = os.getenv("CONDA_EXE")
CONDA_EXE = "conda"


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


def run(cmd: str, cwd=None, shell=False):
    logger.info(f"+ {cmd}")
    subprocess.run(cmd.split(), cwd=cwd, shell=shell)
