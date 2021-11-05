import typer
from pathlib import Path
from pyds.utils import write_file
from ..utils import read_config, run, CONDA_EXE

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
    license: str = typer.Option("MIT", help="Your project's license.", prompt=True),
    auto_create_env: bool = typer.Option(
        True, help="Automatically create environment", prompt=True
    ),
    auto_jupyter_kernel: bool = typer.Option(
        True, help="Automatically expose environment kernel to Jupyter", prompt=True
    ),
):
    """Initialize a new Python data science project."""

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

    if auto_jupyter_kernel:

        cmd = f"eval '$(conda shell.bash hook)' && conda activate {project_name} && python -m ipykernel install --user --name {project_name}"
        run(
            cmd,
            cwd=project_dir,
            shell="/bin/bash",
        )


@app.command()
def update():
    """Update the conda associated with the project."""
    run(f"{CONDA_EXE} clean --all")
    run(f"{CONDA_EXE} env update -f environment.yml")


@app.command()
def reinstall():
    """Rebuild the custom package."""


if __name__ == "__main__":
    app()
