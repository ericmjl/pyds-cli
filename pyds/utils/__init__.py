"""Utility functions for pyds."""
import os
import subprocess
from pathlib import Path
from typing import Dict

import ruamel.yaml
from loguru import logger
from pyprojroot import here
from sh import which

ANACONDA = os.getenv("anaconda", os.getenv("CONDA_PREFIX"))


def read_config():
    """Read PyDS configuration file.

    The PyDS configuration file is always located in the home directory
    and has the name `.pyds.yaml`.

    :returns: A dictionary of PyDS configurations.
    :raises FileNotFoundError: when the pyds config file cannot be found.
    """
    try:
        config_path = Path.home() / ".pyds.yaml"
        yaml = ruamel.yaml.YAML()  # defaults to round-trip

        with config_path.open("r+") as f:
            return yaml.load(f.read())
    except FileNotFoundError:
        raise FileNotFoundError("❗️Please run `pyds configure` to configure pyds!")


def run(
    cmd: str,
    cwd=Path("."),
    shell: bool = True,
    capture_output: bool = True,
    log: bool = True,
    show_out: bool = False,
    activate_env=False,
):
    """Convenience function to run a shell command while also logging the command.

    :param cmd: The command to run.
    :param cwd: The working directory in which to run the code.
    :param shell: Passed to `subprocess.run`'s `shell` argument.
    :param capture_output: Passed to `subprocess.run`'s `capture_output` argument.
    :param log: Whether or not to log the command to screen.
    :param show_out: Whether or not to show the output of `cmd` to the terminal.
    :param activate_env: Whether or not to activate
        the project's conda environment or not before running the command.
        Defaults to False.
    :returns: The result of `subprocess.run`.
    """
    if activate_env:
        env = get_conda_env_name()
        cmd = f"bash -c 'source activate {env} && {cmd}'"
    else:
        cmd = f"bash -c 'source activate base && {cmd}'"
    if log:
        logger.info(f"+ {cmd}")

    run_kwargs = {
        "cwd": cwd,
        "shell": shell,
    }

    if show_out:
        run_kwargs["stdout"] = subprocess.PIPE
    else:
        run_kwargs["capture_output"] = capture_output
    out = subprocess.run(
        cmd,
        **run_kwargs,
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


def discover_conda_executable() -> Path:
    """Discover the conda executable.

    I intend to expand this function
    with other ways of getting the `conda_exe` programmatically.

    :raises Exception: If we cannot find a path to a conda executable.
    :returns: Path to the conda or mamba executable.
    """
    # First, try mamba
    try:
        return which("mamba").strip("\n")
    except Exception:
        pass

    try:
        return which("micromamba").strip("\n")
    except Exception:
        pass

    try:
        return which("conda").strip("\n")
    except Exception:
        pass

    # If `which conda` fails, try using environmenet variables.
    conda_exe = os.getenv("CONDA_EXE")
    if conda_exe is not None:
        return Path(conda_exe)

    raise Exception("Could not find conda executable! Do you have `conda` installed?")


def discover_anaconda_installation() -> Path:
    """Return path to the user's anaconda installation.

    :raises Exception: If we cannot find the path to anaconda installation.
    :returns: Path to anaconda installation directory.
    """
    conda_base_path = os.getenv("CONDA_PREFIX_1")
    if conda_base_path is None:
        conda_base_path = os.getenv("CONDA_PREFIX")
    if conda_base_path is None:
        raise Exception(
            "Could not find path to your anaconda installation! "
            "Do you have `conda` installed?"
        )
    return Path(conda_base_path)


def environment_exists(environment_name: str) -> bool:
    """Function to identify whether an environment exists.

    :param environment_name: The environment of interest.
    :returns: Boolen on whether the expected environment exists.
    """
    conda_base_path = discover_anaconda_installation()
    expected_env_path = conda_base_path / "envs" / environment_name
    return expected_env_path.exists()


CONDA_EXE = discover_conda_executable()
