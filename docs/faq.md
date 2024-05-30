# Frequently Asked Questions

## Source Code Library

> can I access this package in any directory as long as I'm in my project env?

Yes! pyds-cli does a `pip install -e .`, which installs the source code into the conda environment. This means that even if you navigate away from the repository directory, you'll be able to access the package that has been created.

> do changes I make to the source code (which I assume is stored in the project folder) automatically get incorporated for later imports of the source code package

Yes! The source package is installed in editable mode. This means that any code changes are automatically reflected in the installed package, such that when you run a new Python process that uses the library code, they will show up without needing to be re-installed. As a bonus tip, if you use Jupyter notebooks, include the following two lines:

%load_ext autoreload
%autoreload 2

And that will ensure that the Jupyter kernel, which maintains a live Python process, doesn't need to restart in order to see the new code changes.

> I'm also interested in creating sphinx-like documentation for my code, and unsure if pyds-cli does that or something like that out -of-the-box

By default, we have pyds-cli set up to scaffold a mkdocs (documentation system) + mkdocs-material (style) documentation. This allows you to write Markdown for documentation. I've personally tried using sphinx but it's on the "too complex" side for the kinds of documentation that I write, which is the motivation for me to use mkdocs instead.
