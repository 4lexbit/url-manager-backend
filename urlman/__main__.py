import uvicorn

from urlman.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "urlman.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=True,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
