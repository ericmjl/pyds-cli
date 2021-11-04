from typer import Typer
import subprocess


app = Typer()


@app.command()
def build():
    """Build docs for the project."""
    subprocess.run("mkdocs build".split(" "))


@app.command()
def serve():
    """Serve docs for the project."""
    subprocess.run("mkdocs serve".split(" "))


if __name__ == "__main__":
    app()
