from unittest.mock import MagicMock
from result import Ok, Err

import pytest


@pytest.fixture(autouse=True)
def mock_elasticsearch(container):
    from imago.services.elasticsearch.client import ElasticsearchClient

    mock_client: ElasticsearchClient = MagicMock(spec=ElasticsearchClient)
    mock_client.search_media.return_value = Ok([])
    container.elasticsearch_client.override(mock_client)
    yield mock_client
    container.elasticsearch_client.reset_override()


@pytest.mark.anyio
def test_search_empty_query_returns_empty_result(client, mock_elasticsearch):
    response = client.get("/api/media/search")
    assert response.status_code == 200
    assert response.json() == {"results": [], "total": 0}
    mock_elasticsearch.search_media.assert_called_once()


@pytest.mark.anyio
def test_search_media_error_returns_500(client, mock_elasticsearch):
    error_message = "Elasticsearch query failed"
    mock_elasticsearch.search_media.return_value = Err(error_message)

    response = client.get("/api/media/search?q=error")

    assert response.status_code == 500
    assert response.json() == {"detail": error_message}
    mock_elasticsearch.search_media.assert_called_once()
