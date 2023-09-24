# pyper

Pyper is a Python package that offers configuration management capabilities
like the Viper package in Golang.

## Table of Contents

1. [Installation](#installation)

2. [Usage](#usage)

3. [Development](#development)

## Installation

You can install pyper using pip:

```bash
pip install pyper
```

## Usage

### Environment Variables

The `pyper` package provides the `auto_env` function that loads environment
variables from a `.env` file. The function returns a `dict` of all existing
environment variables.

```python
import pyper

env = pyper.auto_env()
```

## Development

We use [Poetry](https://github.com/python-poetry/poetry) for packaging and
dependency management.
After installing Poetry, consider running the command below to configure Poetry
to create virtual environments in a folder named `.venv` within the project's
root directory.

```bash
poetry config virtualenvs.in-project true
```

Afterward, you can run the `install` command to install the dependencies
(including development requirements) specified in the `pyproject.toml` or
`poetry.lock` file.

```bash
poetry install
```

For a more comprehensive description of the Poetry setup and commands, see
their [documentation](https://python-poetry.org/docs).
