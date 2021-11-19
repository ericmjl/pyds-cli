# Opinionated choices

## Dependence on `conda`

The Anaconda distribution of Python has become
the de facto Python distribution recommended for data scientists to use.

## Embracing software development practices

I strongly believe that models, at their core, are software.
Hence, workflows commonly associated with software development,
such as writing tests and documentation,
_ought_ to be part of a data scientist's workflow as well.

## Testing with `pytest`

`pytest` is the modern way to handle software testing.

## Docs with `mkdocs`

MkDocs is a growing and popular alternative to Sphinx,
which has historically been the backbone of Python project documentation.

## Data never live in the repo

Data should never live in the repository.

Data should _never_ live in the repository.

_Data should never, ever live in the repository._

Shipping data _with_ a repository introduces issues with

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
