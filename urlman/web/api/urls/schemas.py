import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from urlman.web.api.transitions.schemas import TransitionOut


class UrlBase(BaseModel):
    """Base Url scheme."""

    url: str
    short_code: Optional[str]
    is_protected: bool = False
    key: Optional[str]

    class Config:
        title = "UrlBaseScheme"
        orm_mode = True
        schema_extra = {
            "example": {
                "url": "https://test.com",
                "short_code": "test_url",
                "is_protected": False,
            },
            "example protected": {
                "url": "https://test.com",
                "short_code": "test_url",
                "is_protected": True,
                "key": "keytoredirect",
            },
        }


class UrlOut(UrlBase):
    """Output Url scheme."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    last_check: Optional[datetime]

    class Config:
        title = "UrlOutputScheme"
        orm_mode = True


class UrlExtended(UrlOut):
    """Output Url scheme."""

    transitions: List[TransitionOut]

    class Config:
        title = "UrlExtendedOutputScheme"
        orm_mode = True


class UrlIn(UrlBase):
    """Input Url scheme."""

    class Config:
        title = "UrlInputScheme"
        orm_mode = True


class UrlUpdate(BaseModel):
    """Update Url scheme."""

    url: Optional[str]
    is_protected: Optional[bool]
    key: Optional[str]

    class Config:
        title = "UrlUpdateScheme"
