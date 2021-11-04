from pathlib import Path
from jinja2 import Template


def read_template(path: Path) -> Template:
    """Return the jinja2 template."""
    with open(path, "r+") as f:
        return Template(f.read())


def write_file(template_file, information, destination_file):
    """Write a template file to disk."""
    template = read_template(template_file)
    text = template.render(**information)
    with open(destination_file, "w+") as f:
        f.write(text)
