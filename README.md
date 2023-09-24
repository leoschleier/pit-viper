# pyper

Pyper is a Python package that offers configuration management
capabilities like the Viper package in Golang.

## Table of Contents

1. [Installation](#installation)

2. [Usage](#usage)

## Installation

You can install pyper using pip:

```bash
pip install pyper
```

## Usage

### Environment Variables

The `pyper` package provides the `auto_env` function that loads
environment variables from a `.env` file. The function returns a `dict`
of all existing environment variables.

```python
import pyper

env = pyper.auto_env()
```
