import uuid
from typing import List, Optional

from pydantic import BaseModel, validate_email, validator

from urlman.web.api.urls.schemas import UrlOut


class UserOut(BaseModel):
    """Output User scheme."""

    id: uuid.UUID
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        title = "UserOutputScheme"
        orm_mode = True


class UserExtended(UserOut):
    """Extended output User scheme."""

    urls: List[UrlOut] = []

    class Config:
        title = "UserExtendedOutputScheme"
        orm_mode = True


class UserIn(BaseModel):
    """Input User scheme."""

    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str

    @validator("email")
    def email_validation(cls, v):
        """Email validation."""
        return validate_email(v)[1]

    class Config:
        title = "UserInputScheme"
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "password1337",
            },
        }


class UserUpdate(UserIn):
    """Update User scheme."""

    username: Optional[str] = None
    email: Optional[str] = None

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


class UserCredentials(BaseModel):
    """User credentials scheme."""

    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        title = "UserCredentialsScheme"
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "password1337",
            },
        }
