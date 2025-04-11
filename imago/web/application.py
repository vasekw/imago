from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from loguru import logger

from imago.log import configure_logging
from imago.settings import settings
from imago.web.api.router import api_router
from imago.web.container import Container
from imago.web.lifespan import lifespan_setup


def create_container() -> Container:
    """Function to create container."""
    container = Container()
    container.config.from_dict(settings.model_dump(), required=True)
    return container


def get_app(container: Container = create_container()) -> FastAPI:
    """Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="imago",
        version=metadata.version("imago"),
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Attach container to app
    app.container = container  # type: ignore
    container.wire(modules=["imago.web.api.media.views"])

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    logger.info("app container initialised")
    return app
