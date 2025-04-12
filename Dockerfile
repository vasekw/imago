FROM python:3.11.4-slim-bullseye AS prod


RUN pip install poetry==1.8.2

# Configuring poetry
RUN poetry config virtualenvs.create false
RUN poetry config cache-dir /tmp/poetry_cache

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

# Copying actuall application
COPY . /app/src/
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

# Expose port 8000 so that it can be accessed outside the container
EXPOSE 8000

CMD ["/usr/local/bin/python", "-m", "imago", "run", "--host", "0.0.0.0"]

FROM prod AS dev

RUN --mount=type=cache,target=/tmp/poetry_cache poetry install
