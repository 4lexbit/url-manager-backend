# urlman

![GitHub](https://img.shields.io/github/license/4lexbit/url-manager-backend?style=flat)
[![Codecov](https://codecov.io/gh/4lexbit/url-manager-backend/branch/main/graph/badge.svg?token=4N5HDVILC8)](https://codecov.io/gh/4lexbit/url-manager-backend)

### Simple service for managing urls: link shortening, viewing visits with ip definition

<hr>

Start a project with:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up
```

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

## Migrations

If you want to migrate your database, you should run following commands:

```bash
# To run all migrations untill the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:

```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:

```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml --project-directory . down
```

For running tests on your local machine.

1. you need to start a database.

I prefer doing it with docker:

```
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=urlman" -e "POSTGRES_USER=urlman" -e "POSTGRES_DB=urlman" postgres:13.4-buster
```

2. Run the pytest.

```bash
pytest -vv .
```
