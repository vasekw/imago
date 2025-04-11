from fastapi.routing import APIRouter

from imago.web.api import media, monitoring, redis

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
