import logging
from typing import List

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search, connections

from imago.services.elasticsearch.utils import build_media_url
from imago.web.api.media.schema import MediaItem

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """Client used to connect to Elasticsearch and elasticsearch_dsl for querying."""

    def __init__(
        self,
        host: str,
        port: int,
        index: str,
        user: str,
        password: str,
    ) -> None:
        self.index = index
        self.client = Elasticsearch(
            hosts=[{"host": host, "port": port, "scheme": "https"}],
            http_auth=(user, password),
            verify_certs=False,  # Insecure: skip SSL verification
        )
        # Register the connection globally for elasticsearch_dsl
        connections.add_connection("default", self.client)

    def search_media(self, query: str, size: int = 10) -> List[MediaItem]:
        """Search using a robust fallback query with elasticsearch_dsl."""
        try:
            # Build the search query
            q = Q("query_string", query=query, fields=[], default_operator="AND")

            s = Search(index=self.index).query(q)[:size]

            response = s.execute()
            media_items = []

            for hit in response:
                item = MediaItem(
                    id=hit.meta.id,
                    image_id=hit.bildnummer,
                    title=hit.suchtext,
                    description=hit.suchtext,
                    db=hit.db,
                    date=hit.datum,
                    photographer=hit.fotografen,
                    width=hit.breite,
                    height=hit.hoehe,
                    thumbnail_url=build_media_url(hit.db, hit.bildnummer),
                )
                media_items.append(item)

            return media_items

        except Exception as e:
            logger.error(f"Elasticsearch DSL search error: {e}")
            return []
