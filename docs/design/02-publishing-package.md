# Publishing the custom source code to a pip server

For a Python data science project,
the work product might be a Python package
that enables your work to be used by other developers,
such as your engineering colleagues or other data scientists.
To publish your package to your pre-configured `internal` pip server,
you can execute the following interactive command:

```bash
pyds publish package --to internal --bump patch
```

Underneath the hood, you'd have to remember at least the following commands
to do a new release:

```bash
bumpversion patch --verbose
rm dist/*
python -m build .
twine upload -r pip-internal dist/
```

That's a lot of jumping between tools!
Instead of having to remember all of them,
now you only have to remember `pyds publish package`.
