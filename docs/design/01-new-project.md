# Creating a new data science project

When creating a new data science project, there are a lot of little details to remember
in order to set up a sane project structure
that supports great practices.
PyDS lets you set all of that up with one interactive command:

```bash
pyds initialize project
```

<script id="asciicast-447988" src="https://asciinema.org/a/447988.js" async></script>

Behind the scenes, we create a new Python project
with an opinionated directory structure.
There's a place to put your `notebooks/`.
There's a custom source directory named after your `project_name/`,
where you can easily refactor out notebook code.
Your `project_name/` source also comes with basic command line interface capabilities
that you can expand on in case you wish to make a CLI tool for others to use.
There are a smattering of code quality tools automatically installed
as part of your `pre-commit` hooks.
You can optionally create a `conda` environment automagically.
