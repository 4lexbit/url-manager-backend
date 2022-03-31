from typing import Optional

from pydantic import BaseModel


class AccessToken(BaseModel):
    """Access JWT token."""

    access_token: Optional[str]
    token_type: str = "bearer"
