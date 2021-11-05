import typer
from ..utils import run

app = typer.Typer()


@app.command()
def publish(
    pypi_server: typer.Option(
        "",
        help="The server name on which to publish the package. (Optional)",
        prompt=True,
    )
):
    """Publish the custom package to a pip-compatible server."""
    run("python -m build .")
    run(f"twine upload -r {pypi_server} dist/")


if __name__ == "__main__":
    app()
