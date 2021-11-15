"""Utility functions for pyds."""
import os
import re
import subprocess
from pathlib import Path
from typing import Dict

import ruamel.yaml
from jinja2 import Template
from loguru import logger
from pyprojroot import here

CONDA_EXE = os.getenv("CONDA_EXE")
ANACONDA = os.getenv("anaconda", os.getenv("CONDA_PREFIX"))


def read_template(path: Path) -> Template:
    """Return the jinja2 template.

    :param path: Path to template.
    :returns: A jinja2 Template object.
    """
    with open(path, "r+") as f:
        return Template(f.read())


def write_file(template_file: Path, information: dict, destination_file: Path):
    """Write a template file to disk.

    :param template_file: Path to a template.
    :param information: Dictionary of information to populate in the template.
    :param destination_file: Path to where the filled template should be placed.
    """
    template = read_template(template_file)
    text = template.render(**information)
    destination_file.touch()
    with destination_file.open(mode="w+") as f:
        f.write(text)


def read_config():
    """Read PyDS configuration file.

    The PyDS configuration file is always located in the home directory
    and has the name `.pyds.yaml`.

    :returns: A dictionary of PyDS configurations.
    :raises Exception: when the pyds config file cannot be found.
    """
    try:
        config_path = Path.home() / ".pyds.yaml"
        yaml = ruamel.yaml.YAML()  # defaults to round-trip

        with config_path.open("r+") as f:
            return yaml.load(f.read())
    except FileNotFoundError:
        raise Exception("❗️Please run `pyds init` to configure pyds!")


def run(
    cmd: str,
    cwd=Path("."),
    shell: bool = True,
    capture_output: bool = True,
    log: bool = True,
    show_out: bool = False,
):
    """Convenience function to run a shell command while also logging the command.

    :param cmd: The command to run.
    :param cwd: The working directory in which to run the code.
    :param shell: Passed to `subprocess.run`'s `shell` argument.
    :param capture_output: Passed to `subprocess.run`'s `capture_output` argument.
    :param log: Whether or not to log the command to screen.
    :param show_out: Whether or not to show the output of `cmd` to the terminal.
    :returns: The result of `subprocess.run`.
    """
    if log:
        logger.info(f"+ {cmd}")

    if show_out:
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


def read_conda_env(env_file="environment.yml", cwd: Path = Path(".")) -> Dict:
    """Load `environment.yml` as a dictionary.

    We try loading from the specified working directory first.
    Otherwise, we use pyprojroot to find the `environment.yml` file.
    If both fail, we raise a loud error.

    :param env_file: The name of the environment file to use.
    :param cwd: The directory in which to look for the environment file.
    :raises NameError: If we are unable to find the environment.yml file.
    :returns: Dictionary containing the conda configuration.
    """
    yaml = ruamel.yaml.YAML()  # defaults to round-trip

    try:
        with open(cwd / env_file, "r+") as f:
            return yaml.load(f.read())
    except FileNotFoundError:
        pass

    try:
        with open(here() / env_file, "r+") as f:
            return yaml.load(f.read())
    except RecursionError:
        pass

    raise NameError(
        "❗️Unable to find environment.yml. Are you inside a project directory?"
    )


# def write_conda_env(env_dict: dict, env_file="environment.yml", cwd: Path = Path(".")):
#     """Write conda environment to disk.

#     This function will always guarantee that we write the `environment.yml` file
#     In the order of:
#     - name
#     - channels
#     - dependencies

#     The function also comes with auxiliary functionality.
#     It will:

#     - ensure that Python is listed at the top of the `dependencies` list.
#     - ensure that the pip section is listed at the bottom of the `dependencies` list.
#     """


def get_conda_env_name(env_file="environment.yml", cwd: Path = Path(".")):
    """Get conda environment name from the environment specification file.

    This function can be executed from anywhere _within_ a project directory.

    We search for `environment.yml` by default.

    :param env_file: Name of the environment file.
    :param cwd: Where to begin recursive search of the project root directory.
    :returns: The environment name.
    """
    env = read_conda_env(env_file=env_file, cwd=cwd)
    return env["name"]


def get_env_bin_dir(env_file="environment.yml", cwd: Path = Path(".")):
    """Get the environment bin directory.

    Used to identify the absolute path to an environment's executables.

    :param env_file: Name of the environment file
        from which we look for the environment name.
    :param cwd: Where to begin recursive search of the project root directory.
    :returns: Path to the conda environment's `bin` directory.
    """
    env_name = get_conda_env_name(env_file=env_file, cwd=cwd)
    ENV_BIN_DIR = f"{ANACONDA}/envs/{env_name}/bin"
    return ENV_BIN_DIR


def to_snake_case(s: str):
    """Change case of a string into snake_case.

    :param s: The string to turn into snake case.
    :returns: Snake-cased string.
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
