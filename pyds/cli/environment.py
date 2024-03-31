"""Commands to help manage your project's development environment.

Scope:

- Environment variables (set in the `.env` file)
- Conda environments (set in the `environment.yml` file).
"""

from typing import Dict

from dotenv import dotenv_values
from pyprojroot import here
from rich import print
from typer import Typer

# from ..utils import read_conda_env

app = Typer()


@app.command()
def set(key: str, value: str):
    """Set a key-value pair in the `.env` file.

    :param key: The name of the environment variable.
    :param value: The value to set the environment variable to.
    """
    env_vars = read_env_vars()
    env_vars[key] = value
    write(env_vars)
    print(f"✅ Successfully set environment variable for {key}! 🎉")


@app.command()
def delete(key: str):
    """Remove an environment variable from the `.env` file.

    :param key: The name of the environment variable.
    """
    env_vars = read_env_vars()
    env_vars.pop(key, None)
    write(env_vars)


@app.command()
def show(keys: bool = True, values: bool = False):
    """Show all environment variables.

    :param keys: Whether to show the keys or not.
    :param values: Whether to show the values or not.
    """
    env_vars = read_env_vars()
    if keys and values:
        print("ℹ️ Here are your environment variables and their values.")
        print(env_vars.items())

    elif keys:
        print("ℹ️ Here are your environment variables without their values.")
        print(env_vars.keys())

    elif values:
        print("ℹ️ Here are your environment variables' values.")
        print(env_vars.values())

    elif not keys and not values:
        print("❌ You probably want to set either keys or values to True!")


def read_env_vars() -> Dict:
    """Read environment variables.

    :returns: A dictionary of environment variables.
    """
    ENV_PATH = here() / ".env"
    return dotenv_values(ENV_PATH)


def write(env_vars: Dict):
    """Write environment variables to disk.

    :param env_vars: A dictionary of environment variables.
    """
    ENV_PATH = here() / ".env"
    with ENV_PATH.open("w+") as f:
        for k, v in sorted(env_vars.items()):
            f.write(f"{k}={v}\n")


# TODO
# @app.command()
# def add_dependency(name: str, conda: bool = True, channel: str = "conda-forge"):
#     pass
#     """Add a dependency to the environment.

#     This command adds a package as a dependency to the `environment.yml` file,
#     and then updates the conda environment
#     based on the newly written `environment.yml` file.

#     Until we have the capability to automatically search for a package via `conda`
#     and know where to add it from,
#     we will
#     """
#     conda_env = read_conda_env()
#     conda_env = add_dependency_package(name)


if __name__ == "__main__":
    app()
