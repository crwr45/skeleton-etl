# skeleton ETL

A not-yet-very-functional skeleton of an ETL process in the mold of
[odoo-edi](https://github.com/mcb30/odoo-edi), but without the Odoo-specific
implementation.

Intended to be backed by a datastore of some description, this is little more
than a code description of the entities and how they should interact.

# Quickstart

Dependencies and venv management is done with [poetry](https://python-poetry.org/)

Use the following to access the venv:
```shell
poetry shell
```

[pre-commit](https://pre-commit.com/) is used for style and linting. Setup:
```shell
pre-commit install
pre-commit run --all
```

# Tests

Uses [pytest](https://docs.pytest.org/en/stable/) to run tests.
```shell
python -m pytest
```
