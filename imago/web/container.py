from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory

from imago.services.elasticsearch.client import ElasticsearchClient


class Container(DeclarativeContainer):
    """Container used dependency injection."""

    config = Configuration()

    # Elasticsearch client
    elasticsearch_client = Factory(
        ElasticsearchClient,
        host=config.elasticsearch_host,
        port=config.elasticsearch_port,
        index=config.elasticsearch_index,
        user=config.elasticsearch_user,
        password=config.elasticsearch_password,
    )
