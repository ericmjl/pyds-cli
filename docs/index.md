# PyDS: A wrapper for creating, configuring, and managing your data science projects

## Why this project exists?

PyDS was born out of the frustration of needing to
memorize commands from a smattering of tools
and repetitively recall a particular folder structure from memory
in order to set up my projects and perform common tasks
(such as Python package publishing).

PyDS follows the philosophy that in order for data scientists to be efficient,
they must have tooling at hand that automates the mundane,
reduces the number of commands that they need to remember,
and makes the sane things easy to do
(that's riff off security folks' mantra, "making the right things easy to do").

In the spirit of automation, this project was thus born.
With it, my aim here is to bring _sanity_ to project initialization.

## Quickstart

Ensure that you have the Anaconda distribution of Python installed,
and that `conda` can be found using your `PATH` environment variable.

Then, install from PyPI:

```bash
pip install pyds
```

For more information, take a look at [the CLI page](./cli) to see what commands exist!

## Design philosophy

PyDS wraps _workflows_.
Workflows are _verbs_ that, underneath the hood,
are implemented by a chain of shell commands.
To read more, see the [Design Philosophy](design/00-index) page
for more details.

## Contributing

To learn how to contribute, head over to the [Contributing](contributing/00-index) page.

## Inspirations

PyDS is inspired by a lot of conversations and reading others' work.
I would like to acknowledge their ideas.

### [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)

Cookiecutter Data Science (CDS)
provided a great starting point for the directory structure.
There are places we deviate from CDS,
such as omitting a `data/` directory,
because in the cloud age,
we should be securely referencing single sources of truth for our data
by way of URIs, s3 buckets (or compatible), database connections, and more.
(My opinion is that data should _not_ live in a project source repository.)
Without CDS, the inspiration for _automation_ would not have existed.

### [Data Science Bootstrap Notes](https://ericmjl.github.io/data-science-bootstrap-notes/)

This is my online book in which I documented a lot of the workflows and best practices
that I developed over my career as a data scientist.
It has some deficiencies, however,
including a focus on _tools_, with insufficient focus on _workflows_.
With PyDS, my goal is to bring the focus back on _workflows_.

### [How to organize your data science project](https://gist.github.com/ericmjl/27e50331f24db3e8f957d1fe7bbbe510)

Many years ago (in 2017, to be precise),
I wrote down my first ideas on the theme of "good data science project organization".
The result was a GitHub gist with a lot of ideas,
but not automation provided.

### Conversations with colleagues at Moderna

My conversations with colleagues on the DSAI team at Moderna
were highly informative for this project.
