# Creating a new data science project

When creating a new data science project, there are a lot of little details to remember
in order to set up a sane project structure
that supports great practices.
PyDS lets you set all of that up with one interactive command:

```bash
pyds project init
```

This command runs [Cookiecutter](https://cookiecutter.readthedocs.io/) against the **[cookiecutter-python-project](https://github.com/ericmjl/cookiecutter-python-project)** template (cloned from GitHub the first time, then cached). To use a local checkout while developing the template, set `PYDS_COOKIECUTTER_PROJECT_TEMPLATE` to that directory, or pass `--template /path/to/cookiecutter-python-project`.

<script id="asciicast-quuvL2LCafmRfpFAbQLREwpke" src="https://asciinema.org/a/quuvL2LCafmRfpFAbQLREwpke.js" async></script>

Behind the scenes, we create a new Python project
with an opinionated directory structure.
There's a place to put your `notebooks/`.
There's a custom source directory named after your `project_name/`,
where you can easily refactor out notebook code.
Your `project_name/` source also comes with basic command line interface capabilities
that you can expand on in case you wish to make a CLI tool for others to use.
There are a smattering of code quality tools automatically installed
as part of your `pre-commit` hooks.
You default to getting a `conda` environment automagically,
and you have a custom Python package (`project_name/`)
installed into the environment too,
ensuring portability of your data analysis code.
