# imago

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m imago
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose up --build
```

If you want to develop in docker with autoreload and exposed ports add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose build
```

## Project structure

```bash
$ tree "imago"
imago
├── __main__.py  # Startup script. Starts uvicorn.
├── settings.py  # Main configuration settings for project.
├── tests  # Tests for project.
    ├── conftest.py  # Fixtures for all tests.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    ├── container.py  # Dependency injector container configuration.
    └── lifespan.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. 

All environment variables should start with "IMAGO_" prefix.

For example if you see in your "imago/settings.py" a variable named like
`random_parameter`, you should provide the "IMAGO_RANDOM_PARAMETER" 
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `imago.settings.Settings.Config`.

To run the application, you **must** set the following environment variables (all with the IMAGO_ELASTICSEARCH_ prefix need to be set):
```bash
IMAGO_RELOAD=True
IMAGO_ELASTICSEARCH_HOST=
IMAGO_ELASTICSEARCH_PORT=
IMAGO_ELASTICSEARCH_INDEX=
IMAGO_ELASTICSEARCH_USER=
IMAGO_ELASTICSEARCH_PASSWORD=
IMAGO_IMAGE_BASE_URL=https://www.imago-images.de/bild
IMAGO_IMAGE_FILE_NAME=s.jpg

```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* ruff (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose run --build --rm api pytest -vv . --cov=. --cov-report=term
docker-compose down
```

For running tests on your local machine.


2. Run the pytest.
```bash
pytest -vv . --cov=. --cov-report=term
```
