from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from imago.services.elasticsearch.client import ElasticsearchClient
from imago.web.api.media.schema import SearchResponse
from imago.web.container import Container

router = APIRouter()


@router.get("/search", response_model=SearchResponse)
@inject
async def get_media(
    q: str = Query(..., description="Search query"),
    size: int = 10,
    es_client: ElasticsearchClient = Depends(Provide[Container.elasticsearch_client]),
) -> SearchResponse:
    """Endpoint to get media from given query.

    q: Search query
    size: Search size
    es_client: ElasticsearchClient

    :return: SearchResponse
    """

    results = es_client.search_media(query=q, size=size)

    return SearchResponse(results=results, total=len(results))
