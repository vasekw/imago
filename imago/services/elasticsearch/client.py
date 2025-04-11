import logging
from typing import List, Optional

from elasticsearch_dsl import Search, connections

from imago.services.elasticsearch.utils import build_media_url
from imago.web.api.media.schema import (
    MediaItem,
    SearchByField,
    SortByField,
    SortDirection,
)

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """Client for interacting with Elasticsearch."""

    def __init__(
        self,
        host: str,
        port: int,
        index: str,
        user: str,
        password: str,
    ) -> None:
        self.index = index
        self.client = connections.create_connection(
            hosts=[{"host": host, "port": port, "scheme": "https"}],
            http_auth=(user, password),
            verify_certs=False,
        )

    def search_media(
        self,
        query: str = "",
        size: int = 10,
        page: int = 1,
        sort_by: SortByField = SortByField.date,
        search_by: Optional[SearchByField] = None,
        sort_direction: SortDirection = SortDirection.asc,
    ) -> List[MediaItem]:
        """Search media for a query."""
        try:
            s = Search(index=self.index)

            if query.strip():
                s = s.query(
                    "query_string",
                    query=query,
                    fields=(
                        [search_by.value]
                        if search_by
                        else [v.value for v in SearchByField]
                    ),
                )
            elif search_by:
                s = s.query("exists", field=search_by.value)

            s = s.sort({f"{sort_by.value}": {"order": sort_direction.value}})
            start = (page - 1) * size
            s = s[start : start + size]

            logger.debug(f"ES Query: {s.to_dict()}")
            response = s.execute()

            return [
                MediaItem(
                    id=hit.meta.id,
                    image_id=getattr(hit, "bildnummer", None),
                    title=getattr(hit, "title", None),
                    description=getattr(hit, "description", None),
                    db=getattr(hit, "db", ""),
                    date=getattr(hit, "datum", None),
                    photographer=getattr(hit, "fotografen", None),
                    width=getattr(hit, "breite", None),
                    height=getattr(hit, "hoehe", None),
                    thumbnail_url=build_media_url(
                        getattr(hit, "db", ""),
                        getattr(hit, "bildnummer", ""),
                    ),
                )
                for hit in response
            ]

        except Exception as e:
            logger.error(f"Elasticsearch DSL search error: {e}")
            return []
