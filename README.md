# CubeCrit

A website for reviewing [speedcubes](https://en.wikipedia.org/wiki/Speedcubing).

## Local Development

### Requirements

- [Python 3.11](https://www.python.org/downloads)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/desktop)
  - You can also install and run [PostgreSQL](https://www.postgresql.org) instead of using the Docker Compose commands

### Commands

```shell
# install dependencies
poetry install

# run formatters/apply fixes
poetry run poe format

# run linters/apply checks
poetry run poe lint

# run tests
poetry run pytest
```

#### Running Locally

```shell
# start the local postgres db server on localhost:5432
docker compose up db

# set environment variables
export DB_ADDRESS="postgresql://cubecrit:password@localhost:5432/cubecrit"

# set environment variables for powershell
$Env:DB_ADDRESS="postgresql://cubecrit:password@localhost:5432/cubecrit"

# start the debug server on localhost:3000
poetry run poe flask-debug
```

## Database Schema

[DB Diagram](https://dbdiagram.io/d/cubecrit-65cad6a6ac844320ae004c73)
