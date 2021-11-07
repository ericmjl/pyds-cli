"""Tools to handle project interactions with pypi."""
import typer
from ..utils import run
from pyprojroot import here

app = typer.Typer()


@app.command()
def publish(
    pip_server: str = typer.Option(
        "",
        help="The name of the server on which to publish the package. Should be configured in your .pypirc.",
        prompt=True,
    )
):
    """Publish the custom package to a pip-compatible server.

    :param pip_server: The name of the server on which to publish the package.
        Should be configured in your .pypirc.
        Can be run from anywhere within the project directory.
    """
    run(f"python -m build {here()}")
    run(f"twine upload -r {pip_server} dist/")


if __name__ == "__main__":
    app()
