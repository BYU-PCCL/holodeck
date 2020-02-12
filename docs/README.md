This folder contains holodeck's user-facing documentation (hosted at
holodeck.readthedocs.io), and is compiled with [Sphinx](http://www.sphinx-doc.org/en/master/).

The documentation can be built locally to preview changes before pushing to
GitHub.

### Prerequisites

`pip install sphinx autodocsumm sphinx_rtd_theme doc8`

### Building

From this directory,
```console
~/dev/holodeck/docs$ make clean && make html
```

[This VSCode extension](https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext)
is useful since it allows you to preview the docs without needing to
compile them.

### Style Note

Pay careful attention to the warnings when you build the docs. The expectation
is that we have a clean build. This includes

Make sure to have the VSCode extension and doc8 installed you you get proper
linting.
