# CubeCrit

A website for reviewing [speedcubes](https://en.wikipedia.org/wiki/Speedcubing).

## Local Development

### Requirements

- [Python 3.11](https://www.python.org/downloads)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/desktop)

### Commands

```shell
# install dependencies
poetry install

# run unit tests
poetry run pytest

# run formatters/apply fixes
poetry run ruff check --fix
poetry run ruff format

# run linters/apply checks
poetry run ruff check
poetry run ruff format --check
poetry run mypy .
```

```shell
# start the local postgres db server on localhost:5432
docker compose up

# set environment variables
export DB_ADDRESS=localhost:5432
export DB_PASSWORD=password

# For Windows Users
$Env:DB_ADDRESS="localhost:5432"
$Env:DB_PASSWORD="password"

# start the debug server on localhost:3000
poetry run flask --app cubecrit run --debug --reload --port 3000
```

## Database Schema

[DB Diagram](https://dbdiagram.io/d/cubecrit-65cad6a6ac844320ae004c73)
