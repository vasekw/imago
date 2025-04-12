import pytest
from unittest.mock import patch
from imago.services.elasticsearch.connection import ElasticsearchConnection


@pytest.fixture
def mock_create_connection():
    with patch("elasticsearch_dsl.connections.create_connection") as mock_connection:
        yield mock_connection


def test_elasticsearch_connection(mock_create_connection):
    # Set up test data
    host = "localhost"
    port = 9200
    user = "test_user"
    password = "test_password"

    es_connection = ElasticsearchConnection(host, port, user, password)

    mock_create_connection.assert_called_once_with(
        hosts=[{"host": host, "port": port, "scheme": "https"}],
        http_auth=(user, password),
        verify_certs=False,
        alias="default",
    )

    assert es_connection.client == mock_create_connection.return_value
