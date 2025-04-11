import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_env_variables(monkeypatch):
    env_vars = {
        "IMAGO_HOST": "127.0.0.1",
        "IMAGO_PORT": "8000",
        "IMAGO_WORKERS_COUNT": "1",
        "IMAGO_RELOAD": "False",
        "IMAGO_ENVIRONMENT": "test",
        "IMAGO_LOG_LEVEL": "INFO",
        "IMAGO_ELASTICSEARCH_HOST": "localhost",
        "IMAGO_ELASTICSEARCH_PORT": "9200",
        "IMAGO_ELASTICSEARCH_INDEX": "test_index",
        "IMAGO_ELASTICSEARCH_USER": "elastic",
        "IMAGO_ELASTICSEARCH_PASSWORD": "password",
    }

    for key, value in env_vars.items():
        monkeypatch.setenv(key, str(value))


@pytest.fixture
def container(mock_env_variables):
    # Delay import so env vars are applied first
    from imago.web.application import create_container

    return create_container()


@pytest.fixture
def app(container):
    from imago.web.application import get_app

    return get_app(container=container)


@pytest.fixture
def client(app):
    return TestClient(app)
