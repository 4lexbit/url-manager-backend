from fastapi.routing import APIRouter

from urlman.web.api import echo, monitoring, urls, users  # , auth

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(urls.router, prefix="/urls", tags=["urls"])
