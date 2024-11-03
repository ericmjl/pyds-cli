# {{ cookiecutter.__project_name }}

{{ cookiecutter.short_description }}

## Development

This project uses `uv` and `juv` for development.
No central environment management is used.
Rather, each notebook has its own development environment.
To modify the dependencies for a notebook,
you can change the `requires-python` and `dependencies` fields in the notebook's header.
