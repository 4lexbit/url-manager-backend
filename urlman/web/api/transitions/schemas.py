from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransitionOut(BaseModel):
    """Output Transition scheme."""

    ip: Optional[str]
    check_time: datetime

    class Config:
        title = "TransitionOutSchema"
        orm_mode = True
