# Opinionated choices

## Dependence on `conda`

The Anaconda distribution of Python has become
the de facto Python distribution recommended for data scientists to use.

## Embracing software development practices

I strongly believe that models, at their core, are software.
Hence, workflows commonly associated with software development,
such as writing tests and documentation,
_ought_ to be part of a data scientist's workflow as well.
As data scientists, if we don't embrace software development ideas,
we set up future personal headache
and barriers to current collaboration.

Software development workflows heavily relies on the concept of
_single sources of truth for stuff_.
This is the spirit behind the term _refactoring_,
where we extract out _stuff_ that might have been copied-and-pasted.
That stuff might be a function that,
after refactoring, we can import and use elsewhere.
It might be a Markdown document that contains units of ideas that we refer to elsewhere.
Or, it might a reference Jupyter notebook
that teaches us the linearized logic of the analysis;
in other words,
an authoritative "report" that forms the basis of our knowledge sharing efforts.
Buying in to "authoritative single sources of truth"
are what prevents us from sloppily duplicating notebooks,
copying and pasting code,
and creating a world of confusion for future selves and collaborators.

## Notebooks are best used for specific purposes

From personal experience and from reading others' experiences,
we've come to the conclusion that notebooks are best used as

1. A space for experimentation and prototyping, and
2. Providing documentation for others.

Usage in any other form makes us _more prone_ to sloppy workflows.
(To be clear, I'm not saying that we are guaranteed to engage in sloppy workflows,
I am merely saying that we will end up with
fewer mental guardrails against sloppy workflows.)

## Custom source code library

Based on the philosophy of "single sources of truth",
PyDS CLI automatically creates a custom source code library
that is automatically installed into the automatically-created conda environment
that is also automatically named in a way that enables you to import into notebooks
and other source code.
By default, this is done as a local, editable install,
enabling you to freely modify the source code and use the new code automatically
without needing to re-install the package each time you make changes.

This source code library is a great place to refactor out code!
For example, if you write a custom PyMC3 or JAX model,
you can stick it into `models.py`.
If you have data preprocessing code, you can stick them into `preprocessing.py`.
And if you want to automatically validate dataframes,
write a [`pandera`](https://pandera.readthedocs.io/en/stable/) schema
and stick it in `schemas.py`!

## Testing with `pytest`

Software testing gives you a contract between current self and others.
By writing a test down,
you're recording what you expect to be the behaviour of a function
at the time of implementation.
If in the future someone changes the function
or changes something that changes the expected inputs of that function,
then a test will help you catch _deviations_ from those expectations.
`pytest` is the modern way to handle software testing,
by abstracting away lots of boilerplate that would otherwise be written
using the built-in `unittest` Python library.

## Docs with `mkdocs`

MkDocs is a growing and popular alternative to Sphinx,
which has historically been the backbone of Python project documentation.
Being able to use pure Markdown to write docs confers a lot of advantages,
but accessibility and ease-of-use is its biggest advantage:
Its syntax is widely-known,
it is easy for newcomers to pick up,
one rarely needs to refer to Markdown documentation to look up syntax,
it is easily portable to other formats (PDF, LaTeX, HTML, etc.),
and for web-targeted documentation,
advanced users can easily mix in custom HTML as necessary.

## Building docs with Jupyter notebooks

Jupyter notebooks are awesome for prototyping and documenting.
By including `mknotebooks` automatically,
we give ourselves the superpower of being able to
include Jupyter notebooks inside our docs.

If paired with a CI/CD bot that _always executes notebooks that are part of docs_,
then suddenly, our docs are _living_ docs,
and can effectively serve as an 'integration test' for our analysis code.

## Data never live in the repo

Data should never live in the repository.

Data should _never_ live in the repository.

_Data should never, ever live in the repository._

In a cloud-first world,
we should be able to reliably store files in a remote location
and pull them into our machine on demand.

## Leverage CI/CD as a _bot_

CI/CD gets bandied about as a fancy term in some circles.
I tend to think of CI/CD in a much, much more simple fashion:
it's a robot. 😅
CI/CD systems, such as GitHub Actions,
are robots that you can program using YAML
(or, gasp! Jenkins) files
rather than Bash scripts alone.
We provide some basic CI/CD files in the form of GitHub Actions configuration files
that automatically provide code checking, testing, and docs building on GitHub.

## GitHub Actions

We target GitHub actions as an opinionated choice.
GitHub Actions hits the right level of abstraction for CI/CD pipelining.
The syntax is easy to learn,
it has easily mix-and-matchable components,
and is free for open source projects.
PyDS CLI ships with GitHub actions that will help you check your code style
and automatically run tests;
you don't have to remember to add them in!
(But feel free to delete these files if they're not necessary;
they're generally harmless outside of GitHub
so we don't bother asking if you want them or not
and instead leave them to you to remove.)

## Pre-commit hooks

We primarily use pre-commit hooks to help you catch code quality issues
before you `git commit` them.
We use the [`pre-commit`](https://pre-commit.com) framework
to manage the code checking tools.
You can think of pre-commit as a bot that runs code checks
before you're allowed to commit the code;
if any fails, you'll be alerted.
We use checkers for docstring coverage,
docstring argument coverage,
code formatting,
and ensuring notebook outputs are _never_ committed.

Using pre-commit can be a bit jarring at first,
because you might have a ton of work being committed.
That said, though, if you commit often and early,
then you'll catch your code quality issues on a faster turnaround cycle,
which makes fixing code issues _much_ easier than otherwise.

## Development Containers

Development containers are another innovation in the developer tooling space
that gives us the ability to work in an even more isolated environment
than pure conda environments alone.
If we were to use Russian Matryoshka dolls (the nested dolls) as an analogy,
Docker-based development containers are the largest doll that ship a computer,
while conda environments are the second largest doll
that ship an isolated Python interpreter.
Development containers work well with VSCode;
we ship an opinionated VSCode dev container Dockerfile definition
that VSCode can automatically discover and build for you.
If dev containers and, more broadly, GitHub codespaces are something you use,
then you'll have no barriers to starting them up.
