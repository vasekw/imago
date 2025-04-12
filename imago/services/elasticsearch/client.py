import logging
from typing import List, Optional

from elasticsearch_dsl import Search
from result import Err, Ok, Result

from imago.services.elasticsearch.connection import ElasticsearchConnection
from imago.web.domain.schema import (
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
        connection: ElasticsearchConnection,
        index: str,
        image_base_url: str,
        image_file_name: str,
    ) -> None:
        self.index = index
        self.client = connection.client
        self.image_base_url = image_base_url
        self.image_file_name = image_file_name

    def _build_media_url(self, db: str, media_id: str) -> str:
        return f"{self.image_base_url}/{db}/{media_id.zfill(10)}/{self.image_file_name}"

    def search_media(
        self,
        query: str = "",
        size: int = 10,
        page: int = 1,
        sort_by: SortByField = SortByField.date,
        search_by: Optional[SearchByField] = None,
        sort_direction: SortDirection = SortDirection.asc,
    ) -> Result[List[MediaItem], str]:
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

            return Ok(
                [
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
                        thumbnail_url=self._build_media_url(
                            getattr(hit, "db", ""),
                            getattr(hit, "bildnummer", ""),
                        ),
                    )
                    for hit in response
                ],
            )

        except Exception as e:
            logger.error(f"Elasticsearch DSL search error: {e}")
            return Err("An error occurred")
