"""Tools to handle project interactions with pypi."""
import typer
from ..utils import run

app = typer.Typer()


@app.command()
def publish(
    pip_server: str = typer.Option(
        "",
        prompt=True,
    )
):
    """Publish the custom package to a pip-compatible server.

    :param pip_server: The name of the server on which to publish the package.
        Should be configured in your .pypirc.
    """
    run("python -m build .")
    run(f"twine upload -r {pip_server} dist/")


if __name__ == "__main__":
    app()
