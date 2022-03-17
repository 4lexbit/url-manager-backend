from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """Application settings."""

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 4
    # Enable uvicorn reloading
    reload: bool = True
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "urlman"
    db_pass: str = "urlman"
    db_base: str = "urlman"
    db_echo: bool = False
    hash_salt: str = "salt1337"
    jwt_issuer: str = "urlman"
    jwt_secret: str = "secret"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    class Config:
        env_file = ".env"
        env_prefix = "URLMAN_"
        env_file_encoding = "utf-8"


settings = Settings()
