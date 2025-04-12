from elasticsearch_dsl import connections


class ElasticsearchConnection:
    """Class for managing Elasticsearch connection."""

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
    ) -> None:
        self.client = connections.create_connection(
            hosts=[{"host": host, "port": port, "scheme": "https"}],
            http_auth=(user, password),
            verify_certs=False,
            alias="default",
        )
