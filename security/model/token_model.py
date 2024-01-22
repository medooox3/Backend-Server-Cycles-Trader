from pydantic import BaseModel
from di import get_settings


config = get_settings()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    admin: bool | None = None
