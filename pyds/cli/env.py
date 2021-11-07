"""Commands to help manage environment variables."""

from typer import Typer
import yaml
from ..utils import run
from dotenv import dotenv_values
from pyprojroot import here
from rich import print

app = Typer()


@app.command()
def set(key: str, value: str):
    """Set a key-value pair in the `.env` file."""
    env_vars = read_env_vars()
    env_vars[key] = value
    write(env_vars)
    print(f"✅ Successfully set environment variable for {key}! 🎉")


@app.command()
def remove(key: str):
    """Remove an environment variable from the `.env` file."""
    env_vars = read_env_vars()
    env_vars.pop(key, None)
    write(env_vars)


@app.command()
def show(keys: bool = True, values: bool = False):
    """Show all environment variables."""
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


def read_env_vars():
    ENV_PATH = here() / ".env"
    return dotenv_values(ENV_PATH)


def write(env_vars):
    """Write environment variables to disk."""
    ENV_PATH = here() / ".env"
    with ENV_PATH.open("w+") as f:
        for k, v in sorted(env_vars.items()):
            f.write(f"{k}={v}\n")


if __name__ == "__main__":
    app()
