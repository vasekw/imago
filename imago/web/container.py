from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Singleton

from imago.services.elasticsearch.client import ElasticsearchClient
from imago.services.elasticsearch.connection import ElasticsearchConnection


class Container(DeclarativeContainer):
    """Container used for dependency injection."""

    config = Configuration()

    # Elasticsearch connection
    elasticsearch_connection = Singleton(
        ElasticsearchConnection,
        host=config.elasticsearch_host,
        port=config.elasticsearch_port,
        user=config.elasticsearch_user,
        password=config.elasticsearch_password,
    )

    # Elasticsearch client
    elasticsearch_client = Factory(
        ElasticsearchClient,
        connection=elasticsearch_connection,
        index=config.elasticsearch_index,
        image_base_url=config.image_base_url,
        image_file_name=config.image_file_name,
    )
