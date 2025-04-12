import pytest
from unittest.mock import MagicMock
from result import Ok, Err
from imago.services.elasticsearch.client import ElasticsearchClient
from imago.services.elasticsearch.connection import ElasticsearchConnection
from unittest.mock import patch, MagicMock
from elasticsearch_dsl import Search
from imago.web.domain.schema import SearchByField, SortByField, SortDirection


@pytest.fixture
def mock_connection():
    connection = ElasticsearchConnection.__new__(ElasticsearchConnection)
    connection.client = MagicMock()
    return connection


@pytest.fixture
def elasticsearch_client(mock_connection):
    return ElasticsearchClient(
        connection=mock_connection,
        index="test-index",
        image_base_url="http://example.com/images",
        image_file_name="preview.jpg",
    )


def test_search_media_with_query(elasticsearch_client):
    mock_hit = MagicMock()
    mock_hit.meta.id = "1"
    mock_hit.bildnummer = "123"
    mock_hit.title = "Test Image"
    mock_hit.description = "A test image"
    mock_hit.db = "archive"
    mock_hit.datum = "2023-01-01"
    mock_hit.fotografen = "Photographer Name"
    mock_hit.breite = 1920
    mock_hit.hoehe = 1080

    with patch("imago.services.elasticsearch.client.Search") as mock_search_class:
        mock_search_instance = MagicMock()
        mock_search_instance.query.return_value = mock_search_instance
        mock_search_instance.sort.return_value = mock_search_instance
        mock_search_instance.__getitem__.return_value = mock_search_instance
        mock_search_instance.execute.return_value = [mock_hit]
        mock_search_instance.to_dict.return_value = {"mock": "query"}

        mock_search_class.return_value = mock_search_instance

        response = elasticsearch_client.search_media(
            query="test",
            size=1,
            page=1,
            sort_by=SortByField.date,
            search_by=SearchByField.title_field,
            sort_direction=SortDirection.desc,
        )

        assert isinstance(response, Ok)
        assert len(response.value) == 1
        result = response.value[0]
        assert result.id == "1"
        assert result.image_id == "123"
        assert result.title == "Test Image"
        assert result.db == "archive"
        assert (
            result.thumbnail_url
            == "http://example.com/images/archive/0000000123/preview.jpg"
        )


def test_search_media_empty_query(elasticsearch_client):
    with patch("imago.services.elasticsearch.client.Search") as mock_search_class:
        mock_search_instance = MagicMock()
        mock_search_instance.query.return_value = mock_search_instance
        mock_search_instance.sort.return_value = mock_search_instance
        mock_search_instance.__getitem__.return_value = mock_search_instance
        mock_search_instance.execute.return_value = []
        mock_search_instance.to_dict.return_value = {"mock": "query"}

        mock_search_class.return_value = mock_search_instance

        results = elasticsearch_client.search_media(
            query="   ", search_by=SearchByField.description
        )

        assert results == Ok([])


def test_search_media_exception(elasticsearch_client):
    with patch("imago.services.elasticsearch.client.Search") as mock_search_class:
        mock_search_instance = MagicMock()
        mock_search_instance.query.side_effect = Exception("Boom!")
        mock_search_class.return_value = mock_search_instance

        results = elasticsearch_client.search_media(query="explode")
        assert isinstance(results, Err)
