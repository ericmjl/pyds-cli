# Design Philosophy

PyDS wraps _workflows_ first; _tools_ are also wrapped, but as a matter of convenience.
_Workflows_ are defined here as a chain of shell commands,
which might involve multiple tools,
that are repetitively executed.
You might be tempted to put those into a Makefile,
and execute them with a single command, `make something`.
That's the kind of workflow that PyDS wraps.

Within a Python data science project, there are workflows that can be automated easily.
These workflows may involve multiple commands;
that's extra headspace to commit to memory.
Here are some workflows supported.

Because workflows are _verbs_, PyDS' internal sub-command structure
is also centered around verbs.
Doing so makes expressing what we want to do much more natural.
Example commands look like:

```bash
pyds project initialize
pyds package publish
pyds docs preview
```

And more generically:

```bash
pyds <thing> <verb>
```

Here, `<thing>` refers to artifacts of some kind.
Documentation (`docs`) are an artifact of the project that we make.
The Python package (`package`) is another artifact.
The project as a whole (`project`) is yet another.

We try to avoid anti-patterns in the implementation.
There is no lock-in with pyds.
We don't implement our own idiosyncratic tools;
literally most of the commands dispatch out to other tools
that we assume to be present on the user's system.
All that `pyds` does is chain them together into higher-order workflows
that follow a natural English expression.
We want to support workflows that compose together tools in the stack;
we don't want to own the stack.
