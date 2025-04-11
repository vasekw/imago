from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from loguru import logger

from imago.services.elasticsearch.client import ElasticsearchClient
from imago.web.api.media.schema import (
    SearchByField,
    SearchResponse,
    SortByField,
    SortDirection,
)
from imago.web.container import Container

router = APIRouter()


@router.get("/search", response_model=SearchResponse)
@inject
async def get_media(
    q: str = Query("", description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = 10,
    sort_by: SortByField = Query(SortByField.date),
    sort_direction: SortDirection = Query(SortDirection.asc),
    search_by: SearchByField | None = Query(None, description="Field to search in"),
    es_client: ElasticsearchClient = Depends(Provide[Container.elasticsearch_client]),
) -> SearchResponse:
    """Endpoint to get media from given query.

    q: Search query
    size: Search size
    es_client: ElasticsearchClient

    :return: SearchResponse
    """
    logger.info(
        f"Search request - q: '{q}', page: {page}, size: {size}, "
        f"sort_by: {sort_by}, search_by: {search_by}",
    )

    results = es_client.search_media(
        query=q,
        size=size,
        page=page,
        sort_by=sort_by,
        sort_direction=sort_direction,
        search_by=search_by,
    )
    return SearchResponse(results=results, total=len(results))
