# {{ cookiecutter.__project_name }}

{{ cookiecutter.short_description }}

## Development

This project uses `uv` and `juv` for development.
No central environment management is used.
Rather, each notebook has its own development environment.
To modify the dependencies for a notebook,
you can change the `requires-python` and `dependencies` fields in the notebook's header.

## Running notebooks

Ensure that you have `juv` installed.
Also ensure that you have `uv` installed.
Then, run any notebook either with `juv run /path/to/notebook.ipynb`
or `pyds analysis run /path/to/notebook.ipynb`.
