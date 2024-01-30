from pydantic import BaseModel, Field
from dependencies import get_settings
from typing import Optional

config = get_settings()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    # user name or admin email
    sub: str 
    # session uuid
    session: Optional[str] = Field(default=None)
