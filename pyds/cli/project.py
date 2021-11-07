"""Project initialization and state management tools."""

from pathlib import Path

import typer

from ..utils import CONDA_EXE, get_env_bin_dir, read_config, run, write_file

THIS_PATH = Path(__file__).parent
TEMPLATE_DIR = THIS_PATH / "templates"

app = typer.Typer()


@app.command()
def init(
    project_name: str = typer.Option(
        ..., help="The project name. Will be snake-cased.", prompt=True
    ),
    project_description: str = typer.Option(
        ..., help="A one-line description of your project.", prompt=True
    ),
    git_remote_url: str = typer.Option("", help="Git remote URL", prompt=True),
    license: str = typer.Option("MIT", help="Your project's license.", prompt=True),
    auto_create_env: bool = typer.Option(
        True, help="Automatically create environment", prompt=True
    ),
    auto_jupyter_kernel: bool = typer.Option(
        True, help="Automatically expose environment kernel to Jupyter", prompt=True
    ),
    auto_pre_commit: bool = typer.Option(
        True, help="Automatically install pre-commit", prompt=True
    ),
):
    """Initialize a new Python data science project.

    :param project_name: Name of the new project to create.
    :param project_description: A one-line description of the project.
    :param git_remote_url: An https or ssh address for the remote project URL.
    :param license: The license to use for your new project. Defaults to "MIT".
    :param auto_create_env: Whether or not to automatically create
        a new conda environment for the project.
        Defaults to True.
    :param auto_jupyter_kernel: Whether or not to automatically expose
        the new Python environment to Jupyter as a Jupyter kernel.
        Defaults to True.
    :param auto_pre_commit: Whether or not to automatically install
        the pre-commit hooks.
        Defaults to True.
    """

    information = dict(
        project_name=project_name,
        project_description=project_description,
        license=license,
    )
    information.update(read_config())

    here = Path.cwd()

    project_dir = here / project_name
    docs_dir = project_dir / "docs"
    tests_dir = project_dir / "tests"
    source_dir = project_dir / project_name

    for directory in [docs_dir, tests_dir, source_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    templates = TEMPLATE_DIR.glob("**/*.j2")

    for template in templates:
        destination_file = project_dir / template.relative_to(TEMPLATE_DIR)
        if "src" in destination_file.parts:
            destination_file = Path(project_dir / project_name / destination_file.name)
        write_file(
            template_file=template,
            information=information,
            destination_file=destination_file.with_suffix(""),
        )

    if auto_create_env:
        run(f"{CONDA_EXE} env update -f environment.yml", cwd=project_dir)

    ENV_BIN_DIR = get_env_bin_dir(cwd=project_dir)
    if auto_jupyter_kernel:
        run(
            f"{ENV_BIN_DIR}/python -m ipykernel install --user --name {project_name}",
            cwd=project_dir,
        )

    run(f"{ENV_BIN_DIR}/pip install -e .", cwd=project_dir)

    run("git init", cwd=project_dir)
    run("git branch -m main", cwd=project_dir)
    run("git add .", cwd=project_dir)
    run("git commit -m 'Initial commit.'", cwd=project_dir)
    run("git add .", cwd=project_dir)
    run("git commit -m 'Initial commit.'", cwd=project_dir)

    if git_remote_url:
        run(f"git remote add origin {git_remote_url}", cwd=project_dir)

    if auto_pre_commit:
        run(f"{ENV_BIN_DIR}/pre-commit install", cwd=project_dir)


@app.command()
def reinstall(
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
