from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi_pagination import add_pagination

from urlman.web.api.router import api_router
from urlman.web.lifetime import shutdown, startup

tags_metadata = [
    {
        "name": "users",
        "description": "**Operations with users**",
    },
]


def get_app() -> FastAPI:
    """:return: FastAPI application."""
    app = FastAPI(
        title="urlman",
        description="URL-managing service",
        contact={
            "name": "Alexey Potapov",
            "email": "alexbit.dev@gmail.com",
        },
        version=metadata.version("urlman"),
        license_info={
            "name": "The MIT License (MIT)",
            "url": "https://mit-license.org/",
        },
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        openapi_tags=tags_metadata,
        default_response_class=UJSONResponse,
    )

    app.on_event("startup")(startup(app))
    app.on_event("shutdown")(shutdown(app))

    app.include_router(router=api_router, prefix="/api")

    add_pagination(app)
    return app
