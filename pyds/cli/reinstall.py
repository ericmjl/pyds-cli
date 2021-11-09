"""Project initialization and state management tools."""


import typer

from ..utils import get_env_bin_dir, run

app = typer.Typer()


@app.command()
def package(
    env_file: str = typer.Option("environment.yml", help="Environment file name.")
):
    """Reinstall the custom package into the conda environment.

    :param env_file: The filename of the conda environment file.
        Defaults to `environment.yml`.
    """
    ENV_BIN_DIR = get_env_bin_dir(env_file)
    run(f"{ENV_BIN_DIR}/python -m pip install -e .")


if __name__ == "__main__":
    app()
