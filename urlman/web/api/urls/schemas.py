import uuid
from typing import Optional

from pydantic import BaseModel


class UrlBase(BaseModel):
    """Base Url scheme."""

    id: uuid.UUID
    url: str
    short_code: str
    is_protected: bool
    key: Optional[str]

    class Config:
        title = "UrlBaseScheme"
        orm_mode = True


class UrlOut(UrlBase):
    """Output Url scheme."""

    class Config:
        title = "UrlOutputScheme"
