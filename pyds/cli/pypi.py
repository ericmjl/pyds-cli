import typer
import subprocess

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
    subprocess.run("python -m build .".split(" "))
    subprocess.run(f"twine upload -r {pypi_server} dist/".split(" "))


if __name__ == "__main__":
    app()
