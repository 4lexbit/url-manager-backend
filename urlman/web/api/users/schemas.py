import uuid
from typing import List, Optional

from pydantic import BaseModel

from urlman.web.api.urls.schemas import UrlBase


class UserOut(BaseModel):
    """Output User scheme."""

    id: uuid.UUID
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        title = "UserOutputScheme"
        orm_mode = True


class UserOutExtended(UserOut):
    """Extended output User scheme."""

    urls: Optional[List[UrlBase]] = None


class UserIn(BaseModel):
    """Input User scheme."""

    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str

    class Config:
        title = "UserInputScheme"
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "password": "password1337",
            },
        }


class UserUpdate(UserIn):
    """Update User scheme."""

    username: Optional[str] = None

    class Config:
        title = "UserUpdateScheme"


class UserChangePassword(BaseModel):
    """Change user password scheme."""

    password: str
    new_password: Optional[str] = None

    class Config:
        title = "UserChangePasswordScheme"
        schema_extra = {
            "example": {
                "password": "password",
                "new_password": "drowssap",
            },
        }
