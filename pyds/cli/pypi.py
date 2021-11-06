import typer
from ..utils import run

app = typer.Typer()


@app.command()
def publish(
    pip_server: typer.Option(
        "",
        help="The server name on which to publish the package. Should be configured in your .pypirc",
        prompt=True,
    )
):
    """Publish the custom package to a pip-compatible server."""
    run("python -m build .")
    run(f"twine upload -r {pip_server} dist/")


if __name__ == "__main__":
    app()
